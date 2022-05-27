import re
from typing import List, Literal

from pydantic import BaseModel, validator
from fastapi import HTTPException


class EmailMessage(BaseModel):
    from_email: str
    to_email: List[str]
    body: str
    type_message: Literal['registration']
