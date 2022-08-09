from tortoise import (
    Model,
    fields,
    transactions,
)
from schemas import (
    extractDB,
)
from models.scripts.superstructures import IntArrayField


class Security(Model):
    id = fields.IntField(pk=True, index=True)
    otp_active = IntArrayField(default=None, null=True)
    phone_active = IntArrayField(default=None, null=True)
    email_active = IntArrayField(default=None, null=True)
    anti_phishing = fields.BooleanField(default=False)
    otp_secret = fields.CharField(max_length=255, null=True)
    user = fields.OneToOneField('models.User', on_delete=fields.CASCADE)

    class Meta:
        table = "security"

    @classmethod
    async def create_otp_secret(cls, user_id: int, url_secret: str) -> dict:
        async with transactions.in_transaction("default") as conn:
            val = await conn.execute_query_dict(f'''
                UPDATE security
                SET otp_secret = $2
                WHERE user_id= $1
                RETURNING security.otp_secret;
            ''', (user_id, url_secret))
            return extractDB(val)

    @classmethod
    async def get_otp_secret(cls, user_id: int) -> dict:
        async with transactions.in_transaction("default") as conn:
            val = await conn.execute_query_dict(f'''
                SELECT otp_secret FROM security
                WHERE user_id= $1;
            ''', (user_id,))
            return extractDB(val)
