import urllib.parse
import pyotp
from typing import (
    Union
)
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from models.security import Security
from schemas import (
    FullSession,
    OperationDetail
)
from resources.render import render_template
from resources.utils import utils
from messages import errors


class GenerateOTP:

    async def __call__(
            self,
            request: Request,
            operation_id: str,
            operation_key:  str,
            code: int,
            _type: str,
            session: FullSession,
    ):
        self._type = _type
        self._code = code
        self._operation_id = str(operation_id)
        self._operation_key = operation_key
        self._session = session
        operation = await self.activate
        if operation:
            session.data.operations[self._operation_id][self._operation_key][_type] = operation
        await utils.backend_memory.update(session_id=session.session_id, data=session.data)
        return RedirectResponse(url=self.url_redirect(request=request))

    @classmethod
    def url_redirect(cls, request: Request):
        url_parts = urllib.parse.urlparse(request.url_for('check_operation'))
        query = dict(request.query_params)
        return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()

    @property
    def get_operation(self) -> OperationDetail:
        try:
            if self._session.data.operations:
                return OperationDetail(
                    **self._session.data.operations[self._operation_id][self._operation_key][self._type]
                )
        except KeyError:
            raise HTTPException(detail='Not valid operation_id or operation_key', status_code=400)

    @property
    async def get_totp(self):
        if self._type == 'otp':
            secret = await Security.get_otp_secret(user_id=self._session.data.user_id)
            totp = pyotp.parse_uri(secret['otp_secret'])
        else:
            secret = self.get_operation.secret
            totp = pyotp.TOTP(secret, interval=300)
        return totp

    @property
    async def activate(self) -> Union[OperationDetail, None]:
        totp = await self.get_totp
        if self._code and totp:
            return self.check_code(totp=totp)
        else:
            if not self.get_operation.active:
                return await self.create_code

    @property
    async def create_code(self):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=300)
        operation = self.get_operation
        operation.secret = secret
        code = totp.now()
        print(code)
        if self._type == 'email':
            body = {
                "to_emails": [self._session.data.general_email],
                "body": render_template(base_html='login.html', **{"code": code}),
                "subject": "Login on an AbsoluteWallet",
            }
            await utils.custom_make_request('send-email', data=body)
        elif self._type == 'sms':
            body = {
              "to_phones": [str(self._session.data.phone)],
              "body": f"Don`t show this code to anyone {code}"
            }
            await utils.custom_make_request('send-sms', data=body)
        return operation

    def check_code(self, totp: pyotp.TOTP):
        try:
            if all((self._code, totp.now() == self._code)):
                operation = self.get_operation
                if operation:
                    operation.active = True
                    return operation
        except TypeError:
            raise errors.not_valid_code


generateOTP = GenerateOTP()
