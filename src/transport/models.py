from tortoise import fields
from tortoise.models import Model
from enum import Enum

class TransportCard(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="transport_cards")
    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    card_number = fields.CharField(max_length=20, unique=True)
    status = fields.CharField(max_length=20, default="active")  # active, blocked, expired

    class Meta:
        table = "transport_cards"


class TransactionType(str, Enum):
    RECHARGE = "recharge"
    DEBIT = "debit"


class TransportTransactionHistory(Model):
    id = fields.IntField(pk=True)
    card = fields.ForeignKeyField("models.TransportCard", related_name="history")
    type = fields.CharEnumField(TransactionType)
    amount = fields.IntField()  
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "transport_transaction_history"
