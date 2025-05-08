from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    document_type: str = Field(..., example="RG")
    file_path: Optional[str] = Field(None, example="/uploads/docs/rg123.pdf")
    file_name: Optional[str] = Field(None, example="rg123.pdf")
    document_number: str = Field(..., example="123456789")

class DocumentCreate(DocumentBase):
    user_id: Optional[int] = Field(None, example=1)

class DocumentUpdate(BaseModel):
    document_type: Optional[str] = Field(None, example="CNH")
    file_path: Optional[str] = Field(None, example="/uploads/docs/cnh987.pdf")
    file_name: Optional[str] = Field(None, example="cnh987.pdf")
    document_number: Optional[str] = Field(None, example="987654321")

class DocumentResponse(DocumentBase):
    id: int = Field(..., example=42)
    user_id: int = Field(..., example=1)
    uploaded_at: datetime = Field(..., example="2025-05-08T14:30:00Z")

    class Config:
        orm_mode = True
