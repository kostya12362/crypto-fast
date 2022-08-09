import json

from typing import (
    Generic,
)

from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel,
)
from fastapi_sessions.frontends.session_frontend import ID

from schemas.session import SessionData

from messages import errors

from settings import config


class InMemoryRedis(Generic[ID, SessionModel], SessionBackend[ID, SessionModel]):

    def __init__(self) -> None:
        self.redis = config.redis_db

    async def create(self, session_id: ID, data: SessionModel):
        if await self.redis.get(str(session_id)):
            raise BackendError("create can't overwrite an existing session")
        await self.redis.set(str(session_id), data.json(exclude_none=True), ex=config.LIVE_SESSION_TIME)

    async def read(self, session_id: ID) -> SessionModel:
        data = await self.redis.get(str(session_id))
        if data:
            return SessionData(**json.loads(data))

    async def update(self, session_id: ID, data: SessionModel, _time: bool = True) -> None:
        if _time:
            await self.redis.set(str(session_id), data.json(exclude_none=True), ex=config.LIVE_SESSION_TIME)
        else:
            sec = await self.redis.ttl(str(session_id))
            await self.redis.set(str(session_id), data.json(exclude_none=True), ex=sec)

    async def delete(self, session_id: ID) -> None:
        if await self.read(session_id=session_id):
            return await self.redis.delete(str(session_id))
        raise errors.session_not_correct
