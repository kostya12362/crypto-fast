from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from schemas import (
    EmailMessage,
    PhoneMessage,
)
from tasks.email import send_email
from tasks.phone import send_phone

from messages import details


router = InferringRouter()


@cbv(router)
class SendAPIView:

    @router.post('/email-message')
    def email_send(self, data: EmailMessage):
        send_email.delay(data.dict())
        return details.message_to_email(data)

    @router.post('/phone-message')
    def phone_send(self, data: PhoneMessage):
        send_phone.delay(data.dict())
        return details.message_to_phone(data)
