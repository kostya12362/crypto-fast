import os
import re
from pydantic import BaseSettings
from typing import Optional

from core.RMQ.client import MicroAsyncClient


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DATABASE: str
    SERVICE_NAME: Optional[str] = '.'.join(re.sub(r'{_x}|\/|.py'.format(_x=BASE_DIR), ' ', os.path.abspath(__file__)).split())

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def get_db_uri(self):
        return f'postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


rb = MicroAsyncClient(prefetch_count=1, service_name=Settings().SERVICE_NAME)
