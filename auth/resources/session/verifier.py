from uuid import UUID
from typing import (
    Tuple,
    Union,
)

from fastapi import HTTPException, Request
from fastapi_sessions.session_verifier import (
    SessionVerifier,
)

from schemas.session import (
    SessionData,
    FullSession
)

from redis.memoery_session import InMemoryRedis

from messages import errors


class SessionTokenVerifier(SessionVerifier[UUID, SessionData]):
    _free_paths_list = (
        '/login/email',
        '/login/google',
        '/login/facebook',
        '/login/telegram',
    )

    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryRedis[UUID, SessionData](),
            auth_http_exception: HTTPException
    ):
        self._session_data: SessionData
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    async def __call__(self, request: Request) -> Union[FullSession, Tuple[SessionData, str]]:
        self.request = request
        self._session_data = await super().__call__(request)
        if self._free_path_check:
            if "Authorization" not in request.headers:
                raise errors.authenticate_not_header
            authorization_header = request.headers['authorization'].split()
            if len(authorization_header) != 2:
                raise errors.authorization_header_token
            if authorization_header[0] != 'Token':
                raise errors.authorization_header_token
            if str(self._session_data.live_token) != authorization_header[1]:
                raise errors.authorization_header_token
        return FullSession(
            data=self._session_data,
            session_id=str(request.state.session_ids[self.identifier])
        )

    @property
    def _free_path_check(self):
        if self.request.url.path not in '|'.join(self._free_paths_list):
            return False
        return True

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        if self._free_path_check:
            return False
        return True
