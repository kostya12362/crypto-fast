from typing import Callable

import aio_pika

QUEUE_ARGUMENTS = {'x-queue-type': 'classic', 'x-max-priority': 5}


class BasicAsyncRMQ:
    def __init__(self):
        self.channel = None
        self.connection = None
        self.queue_arguments = None

    @classmethod
    async def connect(cls, loop, connection_string: str, prefetch_count: int = 5,
                      queue_arguments: dict = None) -> 'BasicAsyncRMQ':
        if queue_arguments is None:
            queue_arguments = QUEUE_ARGUMENTS
        self = BasicAsyncRMQ()
        if connection_string:
            self.connection = await aio_pika.connect_robust(connection_string, loop=loop)
            self.channel = await self.connection.channel()
            self.queue_arguments = queue_arguments
            await self.channel.set_qos(prefetch_count=prefetch_count)
        return self

    async def listen(self, queue_name: str, callback: Callable) -> aio_pika.connection:
        queue = await self.channel.declare_queue(queue_name, durable=True, arguments=self.queue_arguments)
        await queue.consume(callback)
        return self.connection

    async def publish(self, queue_name: str, msg: bytes, headers: dict = None, priority: int = None) -> None:
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=msg, headers=headers, priority=priority),
            routing_key=queue_name
        )

