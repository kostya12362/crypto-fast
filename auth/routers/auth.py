from typing import Tuple, Union
from fastapi import Request, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from schemas import (
    UserCreate,
    FullSession,
    SessionData,
    UserAuthenticateSchema,
    UserDetailSchema,
    EmailAuth,
    SameOperationEnum,
    FacebookSocialAuth,
    GoogleSocialAuth,
    TelegramSocialAuth,
)

from resources import utils, auth, auth_session

router = InferringRouter()


@cbv(router)
class AuthAPIView:

    @router.post(path='/registration', tags=["auth-email"])
    async def registration_user(self, data: UserCreate, session: FullSession = Depends(utils.verifier_cookie)) -> dict:
        response = await auth.email_user_create(data=data, session=session)
        return response

    @router.get(
        path='/email-verify',
        tags=["auth-email"]
    )
    async def email_verify(self, token: str):
        response = await auth.email_user_verify(token=token)
        return response

    @router.post(
        path='/login/email',
        response_model=Union[UserAuthenticateSchema],
        response_model_exclude_unset=True,
        tags=["auth-email"]
    )
    @auth_session.save
    async def login_user(self, data: EmailAuth, session: FullSession = Depends(utils.verifier_cookie)):
        user = await auth.email_user_login(data=data)
        return UserAuthenticateSchema(user=user)

    @router.post(
        path='/login/google',
        response_model=Union[UserAuthenticateSchema],
        response_model_exclude_unset=True,
        tags=['auth-SSO']
    )
    @auth_session.save
    async def login_google(self, data: GoogleSocialAuth):
        response_sso = await utils.google_sso(**data.dict())
        user = await auth.social_user_login_or_create(response_sso)
        return user

    @router.post(
        path='/login/facebook',
        response_model=Union[UserAuthenticateSchema],
        response_model_exclude_unset=True,
        tags=['auth-SSO']
    )
    @auth_session.save
    async def login_facebook(self, data: FacebookSocialAuth, session: FullSession = Depends(utils.verifier_cookie)):
        response_sso = await utils.facebook_sso(**data.dict())
        user = await auth.social_user_login_or_create(response_sso)
        return UserAuthenticateSchema(user=user)

    @router.post(
        path="/login/telegram",
        response_model=Union[UserAuthenticateSchema],
        response_model_exclude_unset=True,
        tags=['auth-SSO'],
    )
    @auth_session.save
    async def login_telegram(self, data: TelegramSocialAuth, session: FullSession = Depends(utils.verifier_cookie)):
        response_sso = await utils.telegram_sso(**data.dict())
        user = await auth.social_user_login_or_create(response_sso)
        return UserAuthenticateSchema(user=user)

    @router.get(
        path="/logout",
        tags=['auth'],
    )
    async def logout(self, session: FullSession = Depends(utils.verifier_cookie)):
        await utils.backend_memory.delete(session_id=session.session_id)
        return {"status": True}

    @router.get(
        path="/test",
    )
    async def test(self, session: FullSession = Depends(utils.verifier_cookie)):
        return session
