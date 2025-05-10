from datetime import date
import pytest
from httpx import AsyncClient
from fastapi import status
from jose import jwt

from src.main import app  
from src.config import auth_settings 
from src.user.models import User

@pytest.mark.anyio
@pytest.mark.integration
async def test_create_document_successfully(client):  
    user = await User.create(
        full_name="João da Silva",
        email="joao.silva@example.com",
        birth_date=date(1990, 5, 20),
        cpf="12345678909",
        phone="11998765432",
        password="SenhaSegura123"
    )
    
    token_payload = {"user_id": user.id}
    token = jwt.encode(token_payload, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    document_payload = {
        "document_type": "RG",
        "file_path": "/uploads/docs/rg123.pdf",
        "file_name": "rg123.pdf",
        "document_number": "123456789"
    }

    response = await client.post("/documents/", json=document_payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["document_type"] == "RG"
    assert data["file_name"] == "rg123.pdf"
    assert data["document_number"] == "123456789"
    assert data["user_id"] == user.id  
    assert "uploaded_at" in data
