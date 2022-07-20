import re
from typing import (
    Optional,
    List,
    Union,
)
from datetime import datetime

from pydantic import (
    BaseModel,
    validator
)


class SecurityControl(BaseModel):
    email_active: Optional[List[int]] = list()
    otp_active: Optional[List[int]] = list()
    phone_active: Optional[List[int]] = list()


class UserDetailSchema(SecurityControl):
    id: int
    general_email: str
    phone: Optional[str]
    date_joined: Optional[datetime]
    is_verified: bool
    anti_phishing: bool
    provider: str

    @validator('general_email', pre=True)
    def format_email(cls, general_email) -> str:
        first, _ = general_email.split('@')
        if len(first) > 2:
            return "@".join([first.replace(first[2:], len(first[2:]) * "*"), _])
        return "@".join([first.replace(first, len(first) * "*"), _])

    @validator('phone', pre=True)
    def format_phone(cls, phone) -> str:
        if phone:
            return phone.replace(phone[4:-2], len(phone[4:-2]) * "*")


class UserAuthenticateSchema(BaseModel):
    user: UserDetailSchema
    token: Optional[str] = None


class OpenID(BaseModel):  # pylint: disable=no-member
    """Class (schema) to represent information got from sso provider in a common form."""
    provider: Optional[str]
    id: Union[str, int] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    picture: Optional[str] = None
    username: Optional[str] = None
