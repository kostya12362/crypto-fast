from typing import Tuple, Union
from fastapi import Request, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from schemas import (
    UserCreate,
    # UserLoginSchema,
    # BaseAuthSchemas,
    FullSession,
    # UserLogin,
    SessionData,
    OperationSchema,
    UserAuthenticateSchema,

    EmailAuth,
    FacebookSocialAuth,
    GoogleSocialAuth,
    TelegramSocialAuth,
)


# from resources.auth.manager import security_module
from resources import utils
from resources import auth

router = InferringRouter()


@cbv(router)
class AuthAPIView:

    @router.post(path='/registration', tags=["auth-email"])
    async def registration_user(self, data: UserCreate, session: FullSession = Depends(utils.verifier_cookie)) -> dict:
        response = await auth.email_user_create(data=data, session=session)
        return response

    @router.get(path='/email-verify', tags=["auth-email"])
    async def email_verify(self, token: str):
        response = await auth.email_user_verify(token=token)
        return response


    @router.post(
        path='/login/email',
        # response_model=Union[UserAuthenticateSchema, OperationSchema],
        response_model_exclude_unset=True,
        tags=["auth-email"]
    )
    async def login_user(self, data: EmailAuth, session: FullSession = Depends(utils.verifier_cookie)):
        user = await auth.email_user_login(data=data)
        # val = await generate_TOTP(session_uuid=session[1], operation_id=1)
        # return val if val else user
        return user

    @router.post(path='/login/google', tags=['auth-SSO'])
    async def login_google(self, data: GoogleSocialAuth, session: SessionData = Depends(utils.verifier_cookie)):
        val = await utils.google_sso(**data.dict())
        # login_or_create_user
        return val

    @router.post(path='/login/facebook', tags=['auth-SSO'])
    async def login_facebook(self, data: FacebookSocialAuth, session: FullSession = Depends(utils.verifier_cookie)):
        val = await utils.facebook_sso(**data.dict())
        user = await auth.social_user_login_or_create(val)
        return user

    @router.post(path="/login/telegram", tags=['auth-SSO'])
    async def login_telegram(self, data: TelegramSocialAuth, session: FullSession = Depends(utils.verifier_cookie)):
        val = await utils.telegram_sso(**data.dict())
        # login_or_create_user

        return val

