import re
import enum
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    validator,
)
from messages import errors
from settings import config


class Provider(enum.Enum):
    email = "email"
    telegram = "telegram"
    facebook = "facebook"
    google = "google"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class EmailAuth(BaseModel):
    email: Optional[str]
    password: Optional[str]

    @validator('email', pre=True)
    def email_valid(cls, email):
        if email and not re.match(r"(^[a-zA-Z\d_.+-]+@[a-zA-Z\d\-]+\.[a-zA-Z\d\-.]+$)", email):
            raise errors.email_not_valid
        return email

    @validator('password')
    def password_validate(cls, password, values):
        if not any((password, values['email'])):
            raise errors.email_provider
        return password


class UserCreate(BaseModel):
    email: str
    password: str
    re_password: str
    redirect_url: str = config.LINK_REDIRECT_VERIFIED

    @validator('email')
    def email_valid(cls, email):
        if not re.match(r"(^[a-zA-Z\d_.+-]+@[a-zA-Z\d\-]+\.[a-zA-Z\d\-.]+$)", email):
            raise errors.email_not_valid
        return email

    @validator('re_password', pre=True, always=True)
    def passwords_match(cls, re_password, values):
        if 'password' in values and re_password != values['password']:
            raise errors.password_match_not_valid
        return re_password


'''
    Social Schemas
'''


class BaseSocialAuth(BaseModel):
    """Main Schemas"""
    token: str


class GoogleSocialAuth(BaseSocialAuth):
    pass


class FacebookSocialAuth(BaseSocialAuth):
    pass


class TelegramSocialAuth(BaseModel):
    auth_date: Optional[str]
    first_name: Optional[str] = None
    hash: Optional[str]
    id: Optional[str]
    last_name: Optional[str] = None
    photo_url: Optional[str] = None
    username: Optional[str] = None
