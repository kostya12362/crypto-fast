import json
import pyotp
import secrets
import pyotp
from typing import List, Union, Optional
from fastapi import Depends, Request, HTTPException
from fastapi.responses import RedirectResponse

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from resources.security.code_message import GenerateOTP
from schemas import (
    SessionData,
    HistoryLoginSchema,
    FullSession,
    SameOperationEnum,
    OperationDetail,
    OperationCheck,
    ActiveTOTP
    # PhoneSchema,
    # AddAntiPhishingSchema,
    # UpdateAntiPhishingSchema,
)

from resources import utils

from models.history_login import HistoryLogin
from models.user import User
from models.security import Security

router = InferringRouter()


@cbv(router)
class SecurityAPIView:

    @router.get('/history_login', )
    async def history_login(self, session: FullSession = Depends(utils.verifier_cookie)) -> List:
        result = await HistoryLogin.select_history_login(session.data.user_id)
        _result = list()
        for item in result:
            _hl = HistoryLoginSchema(**item)
            if await utils.backend_memory.read(_hl.detail[0].session_id):
                _hl.detail[0].active = True
            _result.append(_hl)
        return _result

    @router.get('/add-otp')
    async def create_otp(self, session: FullSession = Depends(utils.verifier_cookie)):
        # print(session.data.user_id)
        secret = pyotp.random_base32()
        # Security.
        url = pyotp.totp.TOTP(secret, interval=180).provisioning_uri(
            name=session.data.general_email,
            issuer_name='AbsoluteWallet'
        )
        val = await Security.create_otp_secret(user_id=session.data.user_id, secret=secret)
        return val, url

    @router.get("/operation")
    async def check_operation(
            self,
            operation_id: int,
            operation_key: Optional[str] = None,
            session: FullSession = Depends(utils.verifier_cookie)
    ):
        if operation_id in SameOperationEnum.list() and session.data.user_id:
            operation_check = OperationCheck(
                email=self._check_in_list(operation_id=operation_id, operation=session.data.email_active),
                otp=self._check_in_list(operation_id=operation_id, operation=session.data.otp_active),
                sms=self._check_in_list(operation_id=operation_id, operation=session.data.phone_active)
            )
            status: str = 'info' if operation_key else 'create'
            if not operation_key:
                operation_key = secrets.token_hex()
                session.data.operations = {
                    str(operation_id): {operation_key: operation_check.dict(exclude_none=True)}
                }
                await utils.backend_memory.update(session_id=session.session_id, data=session.data)
            detail = session.data.operations[str(operation_id)][operation_key]
            # detail.pop('secret', None)
            return {
                'status': status,
                'operation_id': operation_id,
                'operation_key': operation_key,
                'detail': (lambda d: d.pop('secret', d) and d)(detail)
            }
        return "Error"

    @staticmethod
    def _check_in_list(operation_id: int, operation: Union[list] = list) -> Union[OperationDetail, None]:
        if operation_id in operation:
            return OperationDetail()

    @router.get('/operation-email-active', response_class=RedirectResponse, status_code=302)
    async def check_and_send_email(
            self,
            request: Request,
            operation_id: int,
            operation_key: str,
            code: Optional[str] = None,
            session: FullSession = Depends(utils.verifier_cookie)
    ):
        _type = 'email'
        otp = GenerateOTP(request=request, session=session, _type=_type)
        operation = await otp.activate
        if operation:
            session.data.operations[str(operation_id)][operation_key][_type] = operation
        await utils.backend_memory.update(session_id=session.session_id, data=session.data)
        return RedirectResponse(url=otp.url_redirect(request=request))

    @router.get('/operation-sms-active', response_class=RedirectResponse, status_code=302)
    async def check_and_send_sms(
            self,
            request: Request,
            operation_id: int,
            operation_key: str,
            code: Optional[str] = None,
            session: FullSession = Depends(utils.verifier_cookie)
    ):
        _type = 'sms'
        otp = GenerateOTP(request=request, session=session, _type=_type)
        operation = await otp.activate
        if operation:
            session.data.operations[str(operation_id)][operation_key][_type] = operation

        await utils.backend_memory.update(session_id=session.session_id, data=session.data)
        return RedirectResponse(url=otp.url_redirect(request=request))

    @router.get('/operation-otp-active', response_class=RedirectResponse, status_code=302)
    async def check_and_send_sms(
            self,
            request: Request,
            operation_id: int,
            operation_key: str,
            code: Optional[str] = None,
            session: FullSession = Depends(utils.verifier_cookie)
    ):
        _type = 'otp'
        otp = GenerateOTP(request=request, session=session, _type=_type)
        operation = await otp.activate

        if operation:
            session.data.operations[str(operation_id)][operation_key][_type] = operation

        await utils.backend_memory.update(session_id=session.session_id, data=session.data)
        return RedirectResponse(url=otp.url_redirect(request=request))
