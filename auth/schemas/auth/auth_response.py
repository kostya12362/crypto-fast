from typing import (
    Optional,
    List,
    Union,
)
from datetime import datetime

from pydantic import (
    BaseModel,
)


class OperationSecret(BaseModel):
    operation_id: int
    operation_key: Optional[str] = None


class SecurityControl(BaseModel):
    email_active: Union[Optional[List[int]], Optional[bool]] = list()
    otp_active: Union[Optional[List[int]], Optional[bool]] = list()
    phone_active: Union[Optional[List[int]], Optional[bool]] = list()


class UserDetailSchema(SecurityControl):
    id: int
    general_email: Optional[str] = None
    phone: Optional[str]
    date_joined: Optional[datetime]
    is_verified: bool
    anti_phishing: bool
    provider: str = 'email'


class OpenID(BaseModel):
    provider: Optional[str]
    id: Union[str, int] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    picture: Optional[str] = None
    username: Optional[str] = None
