import asyncio
import threading
import smtplib
from settings import (
    rb,
    EMAIL_FROM,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_PORT,
)
from email.mime.text import MIMEText
from sender.tasks import start_spider


class EmailSenderTest:

    def __init__(self):
        loop = asyncio.new_event_loop()
        loop.create_task(rb.main_amqp(loop=loop))
        loop.run_forever()

    @rb(task_name="email")
    async def send_emails(self, *args, **kwargs):
        start_spider.delay("123423sfdgsdg")
        return {"status": "call task celery"}


if __name__ == "__main__":
    EmailSenderTest()
