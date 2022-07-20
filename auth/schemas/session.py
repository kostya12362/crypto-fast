from uuid import UUID

from datetime import (
    datetime,
    timezone,
)
from typing import (
    Optional,
    Dict,
    NamedTuple,
)
from enum import Enum
from pydantic import (
    BaseModel,
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


class SameOperationEnum(Enum):
    login = 1
    swap = 2
    bridge = 3
    change = 4
    security = 5
    settings = 6
    nft = 7
    send = 8


class ActiveTOTP(Dict):

    def __contains__(self, key):
        valid_key = [i.value for i in SameOperationEnum]
        return [key in (list(self.keys()) + valid_key)]

    def __getitem__(self, key):
        if self.__contains__(key):
            return self.___getitem__(self, key)
        else:
            keys = ','.join([f'{i.value}| {i.name}' for i in SameOperationEnum])
            raise KeyError(f'{key} using only {keys}')

    @staticmethod
    def ___getitem__(idict, key):
        if Dict.__contains__(idict, key):
            return Dict.__getitem__(idict, key)


class OperationDetail(BaseModel):
    active: bool = False
    timestamp: Optional[float] = datetime.now(tz=timezone.utc).timestamp()


class OperationCheck(BaseModel):
    sms: Optional[OperationDetail] = None
    email: Optional[OperationDetail] = None
    otp: Optional[OperationDetail] = None


class OperationSchema(BaseModel):
    secret_operation: str
    operation_id: int
    detail: OperationCheck


class SessionData(SecurityControl):
    device: Device
    location: GeoLocation
    ip_address: str
    user_id: Optional[int] = None
    live_token: Optional[UUID] = None
    operation_with_totp: Optional[ActiveTOTP[int, Dict[str, OperationCheck]]]


class FullSession(NamedTuple):
    session_id: str
    data: SessionData

