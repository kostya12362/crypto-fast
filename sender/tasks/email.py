from resources.services import sender_to_email
from . import worker


@worker.task(name='send_email')
def send_email(data):
    for to_email in data['to_emails'].copy():
        data['to_email'] = to_email
        sender_to_email(**data)
