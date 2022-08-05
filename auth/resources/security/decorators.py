# import secrets
# import functools
# from typing import Union
#
# from schemas import (
#     SessionData,
#     SameOperationEnum,
#     OperationDetail,
#     OperationCheck,
#     ActiveTOTP,
#     OperationSchema,
#     OperationSecret,
#     FullSession,
#     UserAuthenticateSchema,
#
# )
# from resources.utils import utils
#
#
# class GenerateOTP:
#
#     @classmethod
#     def otp(cls, operation: SameOperationEnum):
#         def _decorate(func):
#             @functools.wraps(func)
#             async def wrap_func(*args, **kwargs):
#                 session = kwargs['session']
#                 if isinstance(session, FullSession):
#                     if SameOperationEnum.login == operation:
#                         response = await func(*args, **kwargs)
#                         if operation.value in cls._get_active_security_operation(session.data):
#                             _operation = OperationSecret(
#                                 operation_id=operation.value,
#                                 operation_key=secrets.token_hex()
#                             )
#                             _secret_operation = secrets.token_hex()
#                             _operation_check = OperationCheck(
#                                     email=cls._check_in_list(session.data.email_active, operation_id=operation.value),
#                                     otp=cls._check_in_list(session.data.otp_active, operation_id=operation.value),
#                                     sms=cls._check_in_list(session.data.phone_active, operation_id=operation.value)
#                                 )
#                             totp = ActiveTOTP()
#                             totp[operation.value] = {
#                                 _secret_operation: _operation_check.dict(exclude_none=True)
#                             }
#                             session.data.operations = totp
#                             await utils.backend_memory.update(session_id=session.session_id, data=session.data)
#                             return UserAuthenticateSchema(user=response.user, operation=totp[operation.value])
#                         else:
#                             return response
#                     # else:
#                         # if operation.value in cls._get_active_security_operation(session.data):
#                         #     _operation = OperationSecret(operation_id=operation.value,
#                         #                                  operation_secret_key=secrets.token_hex())
#                         #
#                         # else:
#                         #     response = await func(*args, **kwargs)
#                         #     return response
#                 else:
#                     print("error")
#             return wrap_func
#         return _decorate
#
#     @staticmethod
#     def _get_active_security_operation(data: SessionData) -> list:
#         x = list()
#         for k, v in data.dict().items():
#             if k in ('phone_active', 'email_active', 'otp_active') and v:
#                 x += v
#         _set_method = set(x)
#         return [method.value for method in SameOperationEnum if method.value in _set_method]
#
#     # @staticmethod
#     # def _check_in_list(_list_active: Union[list, None], operation_id: int) -> Union[OperationDetail, None]:
#     #     return OperationDetail() if operation_id in _list_active else None
#
#     # async def __call__(self, session_uuid: str, operation_id: int):
#     #     session_data = await utils.backend_memory.read(session_id=session_uuid)
#     #     if operation_id in self._get_active_security_operation(data=session_data):
#     #         _secret_operation = secrets.token_hex()
#     #         _operation_check = OperationCheck(
#     #                 email=self._check_in_list(session_data.email_active, operation_id=operation_id),
#     #                 otp=self._check_in_list(session_data.otp_active, operation_id=operation_id),
#     #                 sms=self._check_in_list(session_data.phone_active, operation_id=operation_id)
#     #             )
#     #         totp = ActiveTOTP()
#     #         totp[operation_id] = {
#     #             _secret_operation: _operation_check.dict(exclude_none=True)
#     #         }
#     #         session_data.operation_with_totp = totp
#     #         await utils.backend_memory.update(session_id=session_uuid, data=session_data)
#     #         return OperationSchema(
#     #             operation_id=operation_id,
#     #             secret_operation=_secret_operation,
#     #             detail=_operation_check
#     #         )
#     #
#     # @staticmethod
#     # def _check_in_list(_list_active: Union[list, None], operation_id: int) -> Union[OperationDetail, None]:
#     #     return OperationDetail() if operation_id in _list_active else None
#     #
#     # @staticmethod
#     # def _get_active_security_operation(data: SessionData):
#     #     _set_method = set(data.phone_active + data.email_active + data.otp_active)
#     #     return (method.value for method in SameOperationEnum if method.value in _set_method)
#
#
# # generate = GenerateOTP()
