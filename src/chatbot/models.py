from tortoise import fields, models
from tortoise.models import Model
from enum import Enum


class IntentEnum(int, Enum):
    CONSULTAR_SALDO = 1
    CANCELAR_CARTAO = 2
    SALVAR_DOCUMENTO = 3
    VER_DOCUMENTOS = 4
    PERGUNTA_LIVRE = 5

class ChatbotState(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="chatbot_states", on_delete=fields.CASCADE)
    
    last_intent = fields.IntEnumField(IntentEnum, null=True)
    
    step = fields.IntField(null=True)
    
    context = fields.JSONField(null=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "chatbot_states"
