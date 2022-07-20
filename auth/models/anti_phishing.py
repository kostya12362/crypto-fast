from tortoise import (
    Model,
    fields,
    transactions,
)


class AntiPhishing(Model):
    id = fields.IntField(pk=True, index=True)
    phrase = fields.CharField(max_length=512, null=True)
    user = fields.OneToOneField('models.Security', on_delete=fields.CASCADE)

    class Meta:
        table = "anti_phishing_phrase"

    @classmethod
    async def insert_phrase(cls, data):
        async with transactions.in_transaction('default') as conn:
            return await conn.execute_query_dict('''
                # SELECT * from select_history_login($1);
            ''', (data.user_id,))