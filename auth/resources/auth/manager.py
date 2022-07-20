from uuid import uuid4
from passlib.context import CryptContext

from fastapi import Request

from models.user import User
from models.history_login import HistoryLogin

from schemas import (
    # UserLoginSchema,
    UserDetailSchema,
    UserAuthenticateSchema,
    SessionData,
    UserCreate,
)

from resources.render import render_template
from resources.security.token import token_manager

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

    # async def create_user(self, data: UserCreate, request: Request) -> dict:
    #     new_user = await User.insert_user(
    #         email=data.email,
    #         password_hash=self.get_password_hash(data.password)
    #     )
    #     if new_user:
    #         session = await utils.backend_memory.read(request.state.session)
    #         token = token_manager.crypto_encode(new_user['id'])
    #         body = {
    #             "to_emails": [
    #                 data.email,
    #             ],
    #             "body": render_template(
    #                 base_html='registration.html',
    #                 **{
    #                     **{
    #                         "redirect_url": data.redirect_url,
    #                         "token": token_manager.crypto_encode(new_user['id']),
    #                     },
    #                     **session.dict()
    #                 }
    #             ),
    #             "subject": "Registration on an AbsoluteWallet",
    #         }
    #         print(f'{data.redirect_url}?token={token}')
    #         response = await utils.custom_make_request(endpoint='send-email', data=body)
    #         return response
    #     else:
    #         # todo log error
    #         raise errors.not_create_user
    #
    # @staticmethod
    # async def user_verified(token: str) -> dict:
    #     try:
    #         user_id = token_manager.crypto_decode(token)
    #     except Exception as e:
    #         # todo add logs
    #         raise errors.token_email_not_valid
    #     if user_id:
    #         val = await User.verified_update(user_id=user_id)
    #         return val
    #     raise errors.token_email_not_valid

    # async def authenticate_user(
    #         self,
    #         body,
    #         session_data: SessionData,
    #         session_uuid: str
    # ) -> UserAuthenticateSchema:
    #     db_user = await User.get_user_by_email(body)
    #     if not self.verify_password(body.password, db_user.get('password_hash')):
    #         raise errors.credential_not_correct
    #     data = UserDetailSchema(**db_user)
    #     if not data.is_verified:
    #         raise errors.not_is_verified
    #     if session_data.user_id:
    #         raise errors.logged_in
    #     return await self.save_to_dbs(session_data, data, session_uuid)

    # @staticmethod
    # async def save_to_dbs(
    #         session_data: SessionData,
    #         user: UserDetailSchema,
    #         session_uuid: str
    # ) -> UserAuthenticateSchema:
    #     try:
    #         await HistoryLogin.insert_history_login(data=session_data, session=session_uuid)
    #         session_data.user_id = user.id
    #         session_data.live_token = uuid4()
    #         values = user.dict()
    #         session_data.phone_active = values.get('phone_active')
    #         session_data.email_active = values.get('email_active')
    #         session_data.otp_active = values.get('otp_active')
    #         await utils.backend_memory.update(session_id=session_uuid, data=session_data, _time=False)
    #         return UserAuthenticateSchema(user=user, token=str(session_data.live_token))
    #     except Exception as e:
    #         # todo add logger
    #         print(e)
    #         raise errors.session_black_list


from schemas import (OpenID, Provider, FullSession, UserCreate, EmailAuth, extractDB)
from typing import Union
from resources.utils_services import utils
from models.user import User


class BaseAuth(Security):

    async def email_user_create(self, data: UserCreate, session: FullSession):
        user = await User.create_user(
            provider=Provider.email.value,
            user_auth={"email": data.email, "password_hash": self.get_password_hash(data.password)}
        )
        token = token_manager.crypto_encode(user['id'])
        body = {
            "to_emails": [
                data.email,
            ],
            "body": render_template(
                base_html='registration.html',
                **{
                    **{
                        "redirect_url": data.redirect_url,
                        "token": token_manager.crypto_encode(user['id']),
                    },
                    **session.data.dict()
                }
            ),
            "subject": "Registration on an AbsoluteWallet",
        }
        print(f'{data.redirect_url}?token={token}')
        response = await utils.custom_make_request(endpoint='send-email', data=body)
        return response

    @staticmethod
    async def email_user_verify(token: str) -> dict:
        try:
            user_id = token_manager.crypto_decode(token)
        except Exception as e:
            # todo add logs
            print(e)
            raise errors.token_email_not_valid
        if user_id:
            val = await User.verified_update(user_id=user_id)
            return val
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
        return UserDetailSchema(**user, provider=provider)

    """
        Social manager
    """

    async def social_user_login_or_create(self, data: OpenID):
        return await User.create_user(provider=data.provider, user_auth=self._skip_provider(data))

    @staticmethod
    def _skip_provider(data: OpenID):
        _d = data.dict()
        _d.pop('provider')
        return _d

    # todo update method login


auth = BaseAuth()
