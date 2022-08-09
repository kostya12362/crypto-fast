import json
from schemas import (extractDB)
from asyncpg.exceptions import RaiseError
from tortoise import (
    Model,
    fields,
    transactions,
)
from messages import errors


class User(Model):
    id = fields.IntField(pk=True, index=True)
    phone = fields.CharField(max_length=200, null=True)
    date_joined = fields.DatetimeField(auto_now=True)
    general_email = fields.CharField(max_length=200, null=True)
    is_verified = fields.BooleanField(default=False)
    user_auth = fields.JSONField(null=True)

    class Meta:
        table = "user"

    @classmethod
    async def create_user(cls, provider: str, user_auth: dict) -> dict:
        async with transactions.in_transaction("default") as conn:
            try:
                val = await conn.execute_query_dict(f'''
                    SELECT * from create_user(provider_new := $1, user_auth_new := $2)
                ''', (provider, json.dumps(user_auth),))
                return extractDB(val)
            except RaiseError:
                raise errors.user_already

    @classmethod
    async def get_user(cls, provider: str, user_auth: dict) -> dict:
        async with transactions.in_transaction("default") as conn:
            val = await conn.execute_query_dict('''
                SELECT * FROM select_user_auth_rows(provider_new := $1, user_auth_new := $2)
            ''', (provider, json.dumps(user_auth),))
            return extractDB(val)

    @classmethod
    async def verified_update(cls, user_id: int) -> dict:
        async with transactions.in_transaction("default") as conn:
            await conn.execute_query_dict(f'''
                UPDATE "user"
                SET is_verified = true
                WHERE id = $1;
                ''', (user_id,))
            val = await conn.execute_query_dict(f'''
                    SELECT * FROM select_user_auth_rows_by_user_id($1);
                ''', (user_id,))

            return extractDB(val)


class TokenAuthBlackList(Model):
    id = fields.IntField(pk=True, index=True)
    auth_token = fields.CharField(max_length=255)

