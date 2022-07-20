from resources.services import sender_to_phone
from . import worker


@worker.task(name='send_phone')
def send_phone(data):
    for to_phone in data['to_phones'].copy():
        data['to_phone'] = to_phone
        sender_to_phone(**data)

