import json
from datetime import datetime
from typing import (
    Optional,
    List,
)
from pydantic import (
    BaseModel,
    validator,
)


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

