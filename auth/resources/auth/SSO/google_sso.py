from .base import BaseSSO
from schemas import (
    Provider,
    OpenID
)


class GoogleSSO(BaseSSO):
    _provider = Provider.google.value
    discovery_url = "https://oauth2.googleapis.com/tokeninfo?id_token={token}"

    async def __call__(self, *args, **kwargs) -> OpenID:
        response = await super().__call__(token=kwargs.get('token'))
        if self.data_check(**{**response, **kwargs}):
            return await self.openid_from_response(response=response)
        raise self.SSOLoginError(401, f"User {response.get('email')} is not verified with Google")

    @classmethod
    async def openid_from_response(cls, response: dict) -> OpenID:
        return OpenID(
            email=response.get("email", ""),
            provider=cls._provider,
            id=response.get("sub"),
            first_name=response.get("given_name"),
            last_name=response.get("family_name"),
            display_name=response.get("name"),
            picture=response.get("picture"),
        )

    @staticmethod
    def data_check(**kwargs):
        if kwargs.get("email_verified"):
            return True
        if kwargs.get('auth_token'):
            return True
