import secrets

from typing import Union

from schemas import (
    SessionData,
    SameOperationEnum,
    OperationDetail,
    OperationCheck,
    ActiveTOTP,
    OperationSchema
)
from resources.utils_services import utils


class GenerateOTP:

    async def __call__(self, session_uuid: str, operation_id: int):
        session_data = await utils.backend_memory.read(session_id=session_uuid)
        if operation_id in self._get_active_security_operation(data=session_data):
            _secret_operation = secrets.token_hex()
            _operation_check = OperationCheck(
                    email=self._check_in_list(session_data.email_active, operation_id=operation_id),
                    otp=self._check_in_list(session_data.otp_active, operation_id=operation_id),
                    sms=self._check_in_list(session_data.phone_active, operation_id=operation_id)
                )
            totp = ActiveTOTP()
            totp[operation_id] = {
                _secret_operation: _operation_check.dict(exclude_none=True)
            }
            session_data.operation_with_totp = totp
            await utils.backend_memory.update(session_id=session_uuid, data=session_data)
            return OperationSchema(
                operation_id=operation_id,
                secret_operation=_secret_operation,
                detail=_operation_check
            )

    @staticmethod
    def _check_in_list(_list_active: Union[list, None], operation_id: int) -> Union[OperationDetail, None]:
        return OperationDetail() if operation_id in _list_active else None

    @staticmethod
    def _get_active_security_operation(data: SessionData):
        _set_method = set(data.phone_active + data.email_active + data.otp_active)
        return (method.value for method in SameOperationEnum if method.value in _set_method)


generate_TOTP = GenerateOTP()
