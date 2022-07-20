from tortoise import (
    Model,
    fields,
    transactions,
)
from schemas import SessionData


class HistoryLogin(Model):
    id = fields.IntField(pk=True, index=True)
    security = fields.ForeignKeyField('models.Security', on_delete=fields.CASCADE, related_name="security", null=True)
    last_login = fields.DatetimeField(auto_now=True)
    session = fields.CharField(max_length=255, unique=True)

    browser = fields.CharField(max_length=255, null=True)
    version = fields.CharField(max_length=255, null=True)
    os_system = fields.CharField(max_length=255, null=True)

    ip_address = fields.CharField(max_length=255, null=True)

    country = fields.CharField(max_length=255, null=True)
    city = fields.CharField(max_length=255, null=True)
    lat = fields.FloatField(null=True)
    long = fields.FloatField(null=True)

    anonymous_user = fields.DatetimeField(null=True)

    class Meta:
        table = "history_login"
        ordering = (
            'security',
            'browser',
            'version',
            'os_system',
            'last_login',
            'ip_address',
            'country',
            'city',
        )

    @classmethod
    async def insert_history_login(cls, data: SessionData, session: str):
        async with transactions.in_transaction('default') as conn:
            await conn.execute_query_dict('''
                INSERT INTO history_login (
                    security_id,
                    city,
                    ip_address,
                    long,
                    os_system,
                    version,
                    country,
                    last_login,
                    lat,
                    browser,
                    anonymous_user,
                    session)
                SELECT
                       s.id as security_id,
                       $2 as city,
                       $3 as ip_address,
                       $4 as long,
                       $5 as os_system,
                       $6 as version,
                       $7 as country,
                       NOW() as last_login,
                       $8 as lat,
                       $9 as browser,
                       NOW() as anonymous_user,
                       $10 as session from public.history_login as hl
                RIGHT JOIN security s ON s.id = hl.security_id
                WHERE s.user_id = $1
                LIMIT 1
            ''', (
                data.user_id,
                data.location.city,
                data.ip_address,
                data.location.long,
                data.device.os_system,
                data.device.version,
                data.location.country,
                data.location.lat,
                data.device.browser,
                session,
            ))
            return True

    @classmethod
    async def select_history_login(cls, user_id: int) -> list:
        async with transactions.in_transaction('default') as conn:
            return await conn.execute_query_dict('''
                SELECT * from select_history_login($1);
            ''', (user_id,))
