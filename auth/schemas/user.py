import re

from pydantic import BaseModel, Field, ValidationError, validator
from fastapi import HTTPException


class UserCreate(BaseModel):
    email: str
    password: str
    re_password: str

    @validator('email')
    def email_valid(cls, email):
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            raise HTTPException(status_code=400, detail='Not valid format email')
        return email

    @validator('re_password', pre=True, always=True)
    def passwords_match(cls, re_password, values, **kwargs):
        if 'password' in values and re_password != values['password']:
            raise HTTPException(status_code=400, detail='Passwords do not match')
        return re_password
