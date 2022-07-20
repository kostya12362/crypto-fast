import re
from typing import List
from pydantic import BaseModel, validator

from messages import errors


class EmailMessage(BaseModel):
    to_emails: List[str]
    body: str
    subject: str

    @validator('to_emails')
    def to_emails_check(cls, to_emails) -> list:
        _to_emails = [i for i in to_emails if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", i)]
        if not _to_emails:
            raise errors.not_valid_to_emails
        return _to_emails
