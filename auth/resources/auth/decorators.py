import functools
from schemas import (
    FullSession,
    UserAuthenticateSchema,
)
from resources.utils import utils
from models.history_login import HistoryLogin


class SaveDataAuth:

    @classmethod
    def save(cls, func):
        def format_email(general_email) -> str:
            if general_email:
                first, _ = general_email.split('@')
                if len(first) > 2:
                    return "@".join([first.replace(first[2:], len(first[2:]) * "*"), _])
                return "@".join([first.replace(first, len(first) * "*"), _])

        def format_phone(phone) -> str:
            if phone:
                return phone.replace(phone[4:-2], len(phone[4:-2]) * "*")

        @functools.wraps(func)
        async def wrap_func(*args, **kwargs):
            response = await func(*args, **kwargs)
            if isinstance(response, UserAuthenticateSchema):
                session: FullSession = kwargs['session']
                await HistoryLogin.insert_history_login(data=session.data, session=session.session_id)
                # response.token = uuid4()
                # session.data.live_token = response.token

                session.data.user_id = response.user.id
                session.data.general_email = response.user.general_email
                session.data.phone = response.user.phone
                session.data.email_active = response.user.email_active
                session.data.phone_active = response.user.phone_active
                session.data.otp_active = response.user.otp_active

                response.user.general_email = format_email(response.user.general_email)
                response.user.phone = format_phone(response.user.phone)


                # session.data.operations = cls._get_active_security_operation(session.data)
                await utils.backend_memory.update(data=session.data, session_id=session.session_id, _time=False)
                return response
        return wrap_func


auth_session = SaveDataAuth()
