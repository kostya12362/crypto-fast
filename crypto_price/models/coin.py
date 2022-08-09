from tortoise import (
    Model,
    fields,
    transactions,
)
from models.scripts.superstructures import VarcharArrayField


class Coin(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=512, null=True)
    symbol = fields.CharField(max_length=512, null=True)
    slug = fields.CharField(max_length=512, null=True)
    tags = VarcharArrayField(null=True)
    cmc_rank = fields.IntField(null=True)
    date_added = fields.DatetimeField(null=True)
    is_active = fields.IntField(null=True)
    prices = fields.JSONField(null=True)

    class Meta:
        table = "coin"

    @classmethod
    def create_or_update(cls):
        return 123
