import httpx
from fastapi import HTTPException


class BaseSSO:
    discovery_url: str = '{token}'

    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id
        self.app_secret = app_secret

    async def __call__(self, token: str = None, *args, **kwargs):
        self._token = token
        async with httpx.AsyncClient() as session:
            response = await session.get(self._make_url_validate)
            content = response.json()
            return content

    @property
    def _make_url_validate(self):
        return self.discovery_url.format(token=self._token)

    class SSOLoginError(HTTPException):
        pass
