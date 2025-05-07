from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentBase(BaseModel):
    document_type: str
    file_path: str
    file_name: str
    document_number: str


class DocumentCreate(DocumentBase):
    user_id: int  # Referência ao ID do usuário


class DocumentUpdate(BaseModel):
    document_type: Optional[str] = None
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    document_number: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
