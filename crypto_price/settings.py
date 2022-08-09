from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):

    BASE_DIR: str = str(Path.cwd())  # base dir detected for render templates

    POSTGRES_PORT: str  # DB port
    POSTGRES_DB: str  # DB name
    POSTGRES_USER: str  # DB user permission
    POSTGRES_PASSWORD: str  # DB password permission
    POSTGRES_HOST: str  # DB host permission if using in docker db else localhost
    POSTGRES_PORT: str  # DB port
    DATABASE: str  # DB type

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def get_db_uri(self):
        return f'postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


config = Settings()
