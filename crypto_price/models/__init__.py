from settings import config
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

TORTOISE_ORM = {
    "connections":
        {
            "default": config.get_db_uri,
        },
    "apps": {
        "models": {
            "models": [
                "models.coin",
                "aerich.models",
            ],
            "default_connection": "default",
        }}
}


def setup_database(app: FastAPI):
    register_tortoise(
        app,
        db_url=config.get_db_uri,
        modules={
            "models": [
                "models.coin",
            ],
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )
