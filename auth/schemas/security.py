import json
from datetime import datetime
from typing import (
    Optional,
    List,
    Dict,
)
from pydantic import (
    BaseModel,
    validator,
)
from schemas.base import SameOperationEnum


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


class TokenEmail(BaseModel):
    id: int
    timestamp: Optional[float] = datetime.now().timestamp()


class SystemDetailSchema(BaseModel):
    id: int
    last_login: str
    location: str
    ip_address: str
    session_id: str
    active: Optional[bool] = False


class HistoryLoginSchema(BaseModel):
    system: Optional[str] = None
    detail: List[SystemDetailSchema]

    @validator('detail', pre=True)
    def validate_user_id(cls, detail: str) -> List[SystemDetailSchema]:
        return [SystemDetailSchema(**i) for i in json.loads(detail)]
