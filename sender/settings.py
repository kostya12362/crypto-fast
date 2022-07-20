from pydantic import BaseSettings
from twilio.rest import Client


class Settings(BaseSettings):
    EMAIL_FROM: str
    EMAIL_HOST: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_PORT: int = 587
    EMAIL_TITLE: str

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    FROM_MOBILE: str

    REDIS_DB: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def get_broker(self) -> str:
        return f'redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'

    @property
    def get_twilio_client(self) -> Client:
        return Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)


config = Settings()
