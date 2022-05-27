import os
import re
from core.RMQ.client import MicroAsyncClient
from pydantic import BaseSettings


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
service_name = '.'.join(re.sub(r'{_x}|\/|.py'.format(_x=BASE_DIR), ' ', os.path.abspath(__file__)).split())
rb = MicroAsyncClient(prefetch_count=1, service_name=service_name)


class Settings(BaseSettings):
    EMAIL_FROM: str
    EMAIL_HOST: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_PORT: int = 587

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



