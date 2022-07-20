from .email_message import *
from .phone_message import *


class ResponseMessage(BaseModel):
    detail: str
