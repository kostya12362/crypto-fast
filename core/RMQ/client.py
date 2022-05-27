import json

from abc import ABC
from aio_pika import IncomingMessage

from core.settings import RMQ_URL_CONNECTION_STR, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASS
from core.RMQ.rmq import BasicAsyncRMQ
from functools import wraps, partial
from typing import Dict
from types import FunctionType
from typing import Optional, TypedDict
from asyncio.events import AbstractEventLoop
from core.RMQ.loggingMircoRMQ import LoggerRMQ
from core.RMQ.models import Message, HeaderRMQ


class ActiveTasks(TypedDict):
    func: FunctionType
    callback: Optional[bool]
    queues: str
    args: Optional[tuple]
    kwargs: Optional[dict]


class MicroAsyncClient(ABC):
    def __init__(self, prefetch_count: int, service_name: str, connection_string: str = RMQ_URL_CONNECTION_STR):
        self.logger = LoggerRMQ(name=service_name)
        self.connection_string: str = connection_string
        self.prefetch_count: int = prefetch_count
        self._con = None
        self.service_name: str = service_name
        self.BRMQ = BasicAsyncRMQ()
        self._reported: Optional[Dict[str, ActiveTasks]] = {}

    def __call__(self, task_name: str, queues: str = "", callback: bool = False, *args, **kwargs):
        def actual_decorator(func):
            self._check_unique_tasks(task_name)
            self._reported[task_name] = ActiveTasks(
                func=func, callback=callback, queues=queues, args=args, kwargs=kwargs
            )

            @wraps(func)
            async def wrapper(*args, **kwargs):
                await func(*args, **kwargs)

            return wrapper

        return actual_decorator

    async def main_amqp(self, loop: AbstractEventLoop):
        self._con = await self.BRMQ.connect(
            loop=loop,
            connection_string=self.connection_string,
            prefetch_count=self.prefetch_count
        )
        await self._con.listen(queue_name=self.service_name, callback=self.on_message)

    async def send(self, message: Message,  priority: int = None):

        print(message.body, message.headers)
        return await self._con.publish(
            msg=message.body.json().encode(),
            headers=json.dumps(message.headers).encode(),
            priority=priority,
            queue_name=message.headers.send_queue
        )

    async def on_message(self, message: IncomingMessage):

        async with message.process():
            decoded_message = message.body.decode()
            try:

                data = json.loads(decoded_message)
                _func = self._reported.get(data['call_task'])['func']
                if _func:
                    args = data['body']['args']
                    kwargs = data['body']['kwargs']
                    result = await _func.__call__(self=self, *args, **kwargs)
                    self.logger.info(f"[x] Received message {decoded_message}")
            except Exception as e:
                self.logger.error(f'{decoded_message} message {e}')

    def _check_unique_tasks(self, _task_name: str):
        if _task_name in set(self._reported.keys()):
            self.logger.error(f"Problem tasks {_task_name}")
            raise ValueError(f"Problem tasks {_task_name}")
