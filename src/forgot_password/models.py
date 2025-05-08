from tortoise import fields
from tortoise.models import Model

class PasswordRecovery(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="recoveries", on_delete=fields.CASCADE)
    recovery_code = fields.CharField(max_length=10)
    recovery_code_expiration = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "password_recoveries"
