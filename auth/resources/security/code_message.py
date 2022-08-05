import urllib.parse
import pyotp
from typing import (
    Union
)
from fastapi import Request, HTTPException
from models.security import Security
from resources import utils
from schemas import (
    FullSession,
    OperationDetail
)
from resources.render import render_template


class GenerateOTP:

    def __init__(self, request: Request, session: FullSession, _type):
        self._type = _type
        self._code = request.query_params.get('code')
        self._operation_id = request.query_params.get('operation_id')
        self._operation_key = request.query_params.get('operation_key')
        self._session = session

    @classmethod
    def url_redirect(cls, request: Request):
        url_parts = urllib.parse.urlparse(request.url_for('check_operation'))
        query = dict(request.query_params)
        return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()

    @property
    def get_operation(self) -> OperationDetail:
        try:
            return OperationDetail(**self._session.data.operations[self._operation_id][self._operation_key][self._type])
        except KeyError:
            raise HTTPException(detail='Not valid operation_id or operation_key', status_code=400)

    @property
    async def activate(self) -> Union[OperationDetail, None]:
        if self._type == 'otp':
            secret = Security.get_otp_secret(self._session.data.user_id)
        else:
            secret = self.get_operation.secret
        if self._code and secret:
            return self.check_code
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

    @property
    def check_code(self):
        totp = pyotp.TOTP(self.get_operation.secret, interval=300)
        if all((self._code, totp.now() == self._code)):
            operation = self.get_operation
            operation.active = True
            return operation
        else:
            raise HTTPException(detail='Not valid code', status_code=400)
