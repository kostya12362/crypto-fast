from pathlib import Path

from pydantic import BaseSettings

from aioredis import (
    Redis,
    from_url,
)


class Settings(BaseSettings):
    SECRET_KEY: str
    TOKEN_LIVE_TIME: int = 1000  # email verify token living 1000 second

    BASE_DIR: str = str(Path.cwd())  # base dir detected for render templates

    POSTGRES_PORT: str  # DB port
    POSTGRES_DB: str  # DB name
    POSTGRES_USER: str  # DB user permission
    POSTGRES_PASSWORD: str  # DB password permission
    POSTGRES_HOST: str  # DB host permission if using in docker db else localhost
    POSTGRES_PORT: str  # DB port
    DATABASE: str  # DB type

    DOMAIN_ENDPOINTS: str = "http://host.docker.internal"  # Other custom API modul in docker

    LINK_REDIRECT_VERIFIED: str = "http://0.0.0.0:5004/auth/email-verify"
    LIVE_SESSION_TIME: int = 3600  # TTL sessions in redis

    REDIS_DB: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    # Google SSO auth
    GOOGLE_REDIRECT_URI: str = 'http://localhost:5004/social-auth/extract/google'
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # Facebook SSO auth
    FACEBOOK_REDIRECT_URI: str = 'http://localhost:5004/social-auth/extract/facebook'
    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def get_db_uri(self):
        return f'postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def get_redis_uri(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    @property
    def redis_db(self) -> Redis:
        return from_url(
            url=self.get_redis_uri,
            password=self.REDIS_PASSWORD,
            encoding="utf-8",
            db=self.REDIS_DB,
            decode_responses=True,
        )


config = Settings()
