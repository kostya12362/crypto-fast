import functools
from uuid import (
    uuid4,
)
from schemas import (
    FullSession,
    UserDetailSchema
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
            if isinstance(response, UserDetailSchema):
                session: FullSession = kwargs['session']
                await HistoryLogin.insert_history_login(data=session.data, session=session.session_id)
                session.data.live_token = str(uuid4())
                session.data.user_id = response.id
                session.data.general_email = response.general_email
                session.data.phone = response.phone
                session.data.email_active = response.email_active
                session.data.phone_active = response.phone_active
                session.data.otp_active = response.otp_active

                response.general_email = format_email(response.general_email)
                response.phone = format_phone(response.phone)
                await utils.backend_memory.update(data=session.data, session_id=session.session_id, _time=False)
                return response
        return wrap_func


auth_session = SaveDataAuth()
