import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import config


class EmailSend:

    def __call__(self, *args, **kwargs):
        self._manager_send_email(
            subject=kwargs['subject'],
            to_email=kwargs['to_email'],
            body=kwargs['body'],
        )

    @staticmethod
    def _manager_send_email(to_email: list, subject: str, body: str):
        sender = f'{config.EMAIL_TITLE}<{config.EMAIL_FROM}>'
        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_FROM, config.EMAIL_HOST_PASSWORD)
            msg['To'] = to_email
            server.sendmail(config.EMAIL_FROM, to_email, msg.as_string())


class PhoneSend:

    def __call__(self, *args, **kwargs):
        config.get_twilio_client.messages.create(
            from_=config.FROM_MOBILE,
            body=kwargs['body'],
            to=kwargs['to_phone']
        )


sender_to_phone = PhoneSend()
sender_to_email = EmailSend()
