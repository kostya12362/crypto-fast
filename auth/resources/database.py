from auth.settings import Settings
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


TORTOISE_ORM = {
    "connections": {"default": Settings().get_db_uri},
    "apps": {
        "models": {
            "models": ["models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def setup_database(app: FastAPI):
    register_tortoise(
        app,
        db_url=Settings().get_db_uri,
        modules={
            'models': ['models.user'],
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )

