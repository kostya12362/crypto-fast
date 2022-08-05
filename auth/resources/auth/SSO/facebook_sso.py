from .base import BaseSSO
from schemas import (
    Provider,
    OpenID
)


class FacebookSSO(BaseSSO):
    _provider = Provider.facebook.value
    discovery_url = "https://graph.facebook.com/v14.0/me?access_token={token}" \
                    "&fields=id,name,email,first_name,last_name,about,picture&format=json" \
                    "&method=get&pretty=0&suppress_http_code=1&transport=cors"

    async def __call__(self, *args, **kwargs) -> OpenID:
        response = await super().__call__(token=kwargs.get('token'))
        if self.data_check(**{**response, **kwargs}):
            return await self.openid_from_response(response=response)
        raise self.SSOLoginError(401, f"User {response.get('email')} is not verified with Facebook")

    @classmethod
    async def openid_from_response(cls, response: dict) -> OpenID:
        """Return OpenID from user information provided by Facebook"""
        return OpenID(
            email=response.get("email", ""),
            provider=cls._provider,
            id=response.get("id"),
            first_name=response.get("first_name"),
            last_name=response.get("last_name"),
            display_name=response.get("name"),
            picture=response.get("picture").get("data").get("url"),
        )

    @staticmethod
    def data_check(**kwargs):
        if kwargs.get('token') and not kwargs.get('error'):
            return True
