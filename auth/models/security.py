from tortoise import (
    Model,
    fields,
)

from models.scripts.superstructures import IntArrayField


class Security(Model):
    id = fields.IntField(pk=True, index=True)
    otp_active = IntArrayField(default=None, null=True)
    phone_active = IntArrayField(default=None, null=True)
    email_active = IntArrayField(default=None, null=True)
    anti_phishing = fields.BooleanField(default=False)
    user = fields.OneToOneField('models.User', on_delete=fields.CASCADE)

    class Meta:
        table = "security"
