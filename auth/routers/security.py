import secrets
import pyotp

from typing import (
    List,
    Union,
    Optional,
)
from fastapi import (
    Depends,
    Request,
)
from fastapi.responses import RedirectResponse
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from schemas import (
    HistoryLoginSchema,
    FullSession,
    SameOperationEnum,
    OperationDetail,
    OperationCheck,
    OperationSchema
)

from resources import utils, generateOTP

from models.history_login import HistoryLogin
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

    @router.get('/add-otp', tags=['OTP'])
    async def create_otp(self, session: FullSession = Depends(utils.verifier_cookie)):
        secret = pyotp.random_base32()
        url_secret = pyotp.totp.TOTP(secret, interval=180).provisioning_uri(
            name=session.data.general_email,
            issuer_name='AbsoluteWallet'
        )
        val = await Security.create_otp_secret(user_id=session.data.user_id, url_secret=url_secret)
        return val, url_secret

    @router.get("/operation", tags=['check-operation'])
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
            ).dict()
            if not operation_key:
                operation_key = secrets.token_hex()
                session.data.operations = {
                    str(operation_id): {operation_key: operation_check}
                }
                await utils.backend_memory.update(session_id=session.session_id, data=session.data)
            detail = session.data.operations.get(str(operation_id), dict()).get(operation_key)
            if detail:
                response = OperationSchema(**{
                    'status': self.validate_status(detail=detail),
                    'operation_id': operation_id,
                    'operation_key': operation_key,
                    'detail': self.replace_key(detail=detail)
                })
                if response.status == 'active' and operation_id == 1:
                    return {"Authorization": f"Token {session.data.live_token}"}
                return response
            else:
                return "Not valid operation_key"
        return "Error"

    @staticmethod
    def replace_key(detail: dict):
        data = dict()
        for k, v in detail.items():
            if v:
                _ = v.pop('secret', v)
                data[k] = v
        return data

    @staticmethod
    def validate_status(detail: dict):
        if all([v.get('active', True) for k, v in detail.items() if v]):
            return 'active'
        else:
            return 'info'

    @staticmethod
    def _check_in_list(operation_id: int, operation: Union[list] = list) -> Union[OperationDetail, None]:
        if operation_id in operation:
            return OperationDetail()

    '''
        send and check code
    '''

    @router.get('/operation-email-active', response_class=RedirectResponse, status_code=302, tags=['check-operation'])
    async def check_and_send_email(
            self,
            request: Request,
            operation_id: int,
            operation_key: str,
            code: Optional[str] = None,
            session: FullSession = Depends(utils.verifier_cookie)

    ):
        return await generateOTP(
            request=request,
            operation_id=operation_id,
            operation_key=operation_key,
            code=code,
            _type='email',
            session=session
        )

    @router.get('/operation-sms-active', response_class=RedirectResponse, status_code=302, tags=['check-operation'])
    async def check_and_send_sms(
            self,
            request: Request,
            operation_id: int,
            operation_key: str,
            code: Optional[str] = None,
            session: FullSession = Depends(utils.verifier_cookie)
    ):
        return await generateOTP(
            request=request,
            operation_id=operation_id,
            operation_key=operation_key,
            code=code,
            _type='sms',
            session=session
        )

    @router.get('/operation-otp-active', response_class=RedirectResponse, status_code=302, tags=['check-operation'])
    async def check_otp_code(
            self,
            request: Request,
            operation_id: int,
            operation_key: str,
            code: str,
            session: FullSession = Depends(utils.verifier_cookie)
    ):
        return await generateOTP(
            request=request,
            operation_id=operation_id,
            operation_key=operation_key,
            code=code,
            _type='otp',
            session=session
        )
