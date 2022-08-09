from passlib.context import CryptContext

from schemas import (
    OpenID,
    Provider,
    FullSession,
    UserCreate,
    EmailAuth,
    UserDetailSchema
)

from models.user import User

from resources.render import render_template
from resources.security.token import token_manager
from resources.utils import utils

from messages import errors


#
#
class Security:

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


class BaseAuth(Security):

    async def email_user_create(self, data: UserCreate, session: FullSession):
        user = await User.create_user(
            provider=Provider.email.value,
            user_auth={"email": data.email, "password_hash": self.get_password_hash(data.password)}
        )
        token = token_manager.crypto_encode(user['id'])
        content = {
            **{"redirect_url": data.redirect_url, "token": token_manager.crypto_encode(user['id'])},
            **session.data.dict()
        }
        body = {
            "to_emails": [data.email],
            "body": render_template(base_html='registration.html', **content),
            "subject": "Registration on an AbsoluteWallet",
        }
        print(f'{data.redirect_url}?token={token}')
        response = await utils.custom_make_request(endpoint='send-email', data=body)
        return response

    @staticmethod
    async def email_user_verify(token: str) -> UserDetailSchema:
        try:
            user_id = token_manager.crypto_decode(token)
        except Exception as e:
            # todo add logs
            print(e)
            raise errors.token_email_not_valid
        if user_id:
            val = await User.verified_update(user_id=user_id)
            return UserDetailSchema(**val)
        raise errors.token_email_not_valid

    async def email_user_login(self, data: EmailAuth) -> UserDetailSchema:
        provider = Provider.email.value
        user = await User.get_user(
            provider=provider,
            user_auth=data.dict()
        )
        password_hash = user['user_auth'][provider]
        if not user['is_verified']:
            raise errors.not_is_verified
        if not self.verify_password(data.password, password_hash.get('password_hash')):
            raise errors.credential_not_correct
        return UserDetailSchema(provider=provider, **user)

    """
        Social manager
    """
    async def social_user_login_or_create(self, data: OpenID) -> UserDetailSchema:
        user = await User.create_user(provider=data.provider, user_auth=self._skip_provider(data))
        return UserDetailSchema(provider=data.provider, **user)

    @staticmethod
    def _skip_provider(data: OpenID):
        _d = data.dict()
        _d.pop('provider')
        return _d

    # todo update method login


auth = BaseAuth()
