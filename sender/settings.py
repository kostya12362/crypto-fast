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


EMAIL_FROM = os.getenv('EMAIL_HOST_USER', 'pre-listing@cryptobot.page')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.office365.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'gdshxhzfwqcnvdsz')
EMAIL_PORT = 587


