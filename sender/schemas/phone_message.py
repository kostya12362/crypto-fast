from typing import List

from twilio.base.exceptions import TwilioRestException

from pydantic import BaseModel, validator

from settings import config

from messages import errors


class PhoneMessage(BaseModel):
    to_phones: List[str]
    body: str

    @validator('to_phones')
    def to_emails_check(cls, to_phones) -> list:
        data = list()
        for phone in to_phones:
            try:
                config.get_twilio_client.lookups.phone_numbers(phone).fetch(type="carrier")
                data.append(phone)
            except TwilioRestException as e:
                if e.code == 20404:
                    raise errors.not_valid_to_phone
                else:
                    raise e
        return data
