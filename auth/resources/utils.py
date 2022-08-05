import json

import httpx
from typing import (
    Literal,
    Optional,
)
from uuid import UUID
from pydantic import (
    BaseModel,
    validator,
)

from fastapi_sessions.frontends.implementations import (
    SessionCookie,
    CookieParameters,
)

from redis.memoery_session import InMemoryRedis
from schemas import SessionData

from resources.session.verifier import SessionTokenVerifier
from resources import (
    GoogleSSO,
    TelegramSSO,
    FacebookSSO,
)
from messages import errors
from settings import config


class UtilsServices:

    class URLPath(BaseModel):
        path: str
        method: Literal['POST', 'GET']

    ENDPOINTS = {
        'send-email': URLPath(path='http://localhost:5005/send/email-message', method='POST'),
        'send-sms': URLPath(path='http://localhost:5005/send/phone-message', method='POST'),
        'ip-detail': URLPath(path='http://www.geoplugin.net/json.gp?ip={ip_address}', method='GET')
    }

    async def custom_make_request(
            self,
            endpoint: str,
            data: Optional[dict] = None,
            parameters: Optional[dict] = dict
    ) -> dict:
        async with httpx.AsyncClient() as client:
            _e = self.ENDPOINTS.get(endpoint)
            if _e:
                if _e.method == 'POST':
                    response = await client.post(url=self.ENDPOINTS[endpoint].path, json=data)
                elif _e.method == 'GET':
                    response = await client.get(url=self.ENDPOINTS[endpoint].path.format(**parameters))
        return json.loads(response.text)

    @property
    def backend_memory(self):
        return InMemoryRedis[UUID, SessionData]()

    @property
    def cookie_session(self):
        cookie_params = CookieParameters()
        cookie_params.max_age = 100000
        return SessionCookie(
            cookie_name="session",
            identifier="general_verifier",
            auto_error=True,
            secret_key=config.SECRET_KEY,
            cookie_params=cookie_params,
        )

    @property
    def verifier_cookie(self):
        return SessionTokenVerifier(
            identifier="general_verifier",
            auto_error=True,
            backend=self.backend_memory,
            auth_http_exception=errors.session_not_correct,
        )

    @property
    def google_sso(self):
        return GoogleSSO()

    @property
    def facebook_sso(self):
        return FacebookSSO()

    @property
    def telegram_sso(self):
        return TelegramSSO(
            app_id='1750459114',
            app_secret='AAH8yZdI0Px1nZB0DqeRNIQyy47CkMmZQZ8'
        )


utils = UtilsServices()
