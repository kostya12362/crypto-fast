from uuid import UUID
from datetime import (
    datetime,
    timezone,
)
from typing import (
    Optional,
    NamedTuple,
)
from pydantic import (
    BaseModel,
    validator,
)
from schemas.auth.auth_response import SecurityControl


class Device(BaseModel):
    browser: Optional[str] = None
    version: Optional[str]
    os_system: Optional[str]


class GeoLocation(BaseModel):
    country: str
    city: str
    lat: Optional[float]
    long: Optional[float]


class OperationDetail(BaseModel):
    active: bool = False
    timestamp: Optional[float] = datetime.now(tz=timezone.utc).timestamp()
    secret: Optional[str] = None


class OperationCheck(BaseModel):
    sms: Optional[OperationDetail] = None
    email: Optional[OperationDetail] = None
    otp: Optional[OperationDetail] = None


class OperationSchema(BaseModel):
    status: Optional[str] = 'info'
    operation_key: str
    operation_id: int
    detail: OperationCheck


class SessionData(SecurityControl):
    device: Device
    location: GeoLocation
    ip_address: str
    general_email: str = None
    phone: str = None
    user_id: Optional[int] = None
    live_token: Optional[UUID] = None
    operations: Optional[dict] = None


class FullSession(NamedTuple):
    session_id: str
    data: SessionData
