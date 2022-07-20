import hashlib
import hmac
from .base import BaseSSO
from schemas import (
    Provider,
    OpenID
)


class TelegramSSO(BaseSSO):
    _provider = Provider.telegram.value

    async def __call__(self, *args, **kwargs) -> OpenID:
        if self.data_check(**kwargs):
            return await self.openid_from_response(response=kwargs)
        raise self.SSOLoginError(401, f"User {kwargs.get('username')} is not verified with Telegram")

    @classmethod
    async def openid_from_response(cls, response: dict) -> OpenID:
        return OpenID(
            provider=cls._provider,
            id=response.get("id"),
            first_name=response.get("first_name"),
            last_name=response.get("last_name"),
            picture=response.get("photo_url"),
            username=response.get("username")
        )

    @staticmethod
    def string_generator(**kwargs):
        data = kwargs.copy()
        del data['hash']
        return '\n'.join([f'{k}={v}' for k, v in sorted(data.items())])

    def data_check(self, **kwargs):
        hmac_string = hmac.new(
            hashlib.sha256(f'{self.app_id}:{self.app_secret}'.encode('utf-8')).digest(),  # secret
            bytes(self.string_generator(**kwargs), 'utf-8'),
            hashlib.sha256
        ).hexdigest()
        if hmac_string == kwargs['hash']:
            return True
