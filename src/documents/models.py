from tortoise import fields
from tortoise.models import Model

class Document(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="documents")
    document_type = fields.CharField(max_length=50) 
    file_path = fields.CharField(max_length=255, null=True)    
    file_name = fields.CharField(max_length=255, null=True)
    document_number = fields.CharField(max_length=50)
    uploaded_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "documents"
