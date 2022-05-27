
from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    # password = fields.CharField(max_length=200)
    phone = fields.CharField(max_length=200, null=True)
    is_verified = fields.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        table = "user"
