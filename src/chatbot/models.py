from tortoise import fields
from tortoise.models import Model
from enum import Enum, auto
from tortoise.fields import CharEnumField

class ChatNodeType(str, Enum):
    ROOT = 'root'
    MENU = 'menu'
    LEAF = 'leaf'

class ChatSession(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='chat_sessions')
    current_node_id = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_interaction_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = 'chat_sessions'

class ChatInteraction(Model):
    id = fields.IntField(pk=True)
    chat_session = fields.ForeignKeyField('models.ChatSession', related_name='interactions')
    node_id = fields.CharField(max_length=100)
    user_selection = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'chat_interactions'

class ChatbotNode(Model):
    id = fields.CharField(max_length=100, pk=True)
    parent_id = fields.CharField(max_length=100, null=True)
    type = fields.CharEnumField(ChatNodeType)
    message = fields.TextField()
    options = fields.JSONField(default=list)  # Store options as JSON

    class Meta:
        table = 'chatbot_nodes'
