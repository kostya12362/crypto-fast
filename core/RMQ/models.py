from pydantic import BaseModel
from typing import Optional, TypedDict


class HeaderRMQ(BaseModel):
    call_task: str
    send_queue: str


class BodyMessageRMQ(BaseModel):
    args: Optional[tuple]
    kwargs: Optional[dict]


class Message(BaseModel):
    body: BodyMessageRMQ
    headers: HeaderRMQ

