from datetime import date
import pytest
from httpx import AsyncClient
from fastapi import status
from jose import jwt

from src.documents.models import Document
from src.main import app  
from src.config import auth_settings 
from src.user.models import User

@pytest.mark.anyio
@pytest.mark.integration
async def test_create_document_successfully(client):  
    await User.all().delete()
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

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_document_success(client: AsyncClient):
    await User.all().delete()
    user = await User.create(
        full_name="Maria Souza",
        email="maria@example.com",
        birth_date=date(1992, 3, 15),
        cpf="98765432100",
        phone="11912345678",
        password="SenhaForte456"
    )

    token_payload = {"user_id": user.id}
    token = jwt.encode(token_payload, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG)
    headers = {"Authorization": f"Bearer {token}"}

    document = await Document.create(
        document_type="CNH",
        file_path="/uploads/docs/cnh999.pdf",
        file_name="cnh999.pdf",
        document_number="987654321",
        user_id=user.id
    )

    response = await client.get(f"/documents/{document.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == document.id
    assert data["document_type"] == "CNH"

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_document_not_found(client: AsyncClient):
    await User.all().delete()
    user = await User.create(
        full_name="Maria Souza",
        email="maria2@example.com",
        birth_date=date(1992, 3, 15),
        cpf="14781951775",
        phone="11912345678",
        password="SenhaForte456"
    )

    token_payload = {"user_id": user.id}
    token = jwt.encode(token_payload, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/documents/9999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Documento não encontrado."
    
@pytest.mark.anyio
@pytest.mark.integration
async def test_update_document_success(client: AsyncClient):
    await User.all().delete()
    user = await User.create(
        full_name="João da Silva",
        email="joao@example.com",
        birth_date=date(1990, 1, 1),
        cpf="12345678900",
        phone="11999999999",
        password="SenhaSegura123"
    )

    token_payload = {"user_id": user.id}
    token = jwt.encode(token_payload, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG)
    headers = {"Authorization": f"Bearer {token}"}

    document = await Document.create(
        document_type="RG",
        file_path="/uploads/docs/rg123.pdf",
        file_name="rg123.pdf",
        document_number="123456789",
        user_id=user.id
    )

    update_payload = {
        "document_type": "CNH",
        "file_path": "/uploads/docs/cnh987.pdf",
        "file_name": "cnh987.pdf",
        "document_number": "987654321"
    }

    response = await client.put(f"/documents/{document.id}", json=update_payload, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == document.id
    assert data["document_type"] == "CNH"
    assert data["file_path"] == "/uploads/docs/cnh987.pdf"
    assert data["file_name"] == "cnh987.pdf"
    assert data["document_number"] == "987654321"
    
@pytest.mark.anyio
@pytest.mark.integration
async def test_update_document_not_found(client: AsyncClient):
    await User.all().delete()
    user = await User.create(
        full_name="Carlos Oliveira",
        email="carlos@example.com",
        birth_date=date(1985, 6, 20),
        cpf="11223344556",
        phone="11988888888",
        password="SenhaForte321"
    )

    token_payload = {"user_id": user.id}
    token = jwt.encode(token_payload, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG)
    headers = {"Authorization": f"Bearer {token}"}

    update_payload = {
        "document_type": "CNH",
        "file_path": "/uploads/docs/cnh999.pdf",
        "file_name": "cnh999.pdf",
        "document_number": "999999999"
    }

    response = await client.put("/documents/9999", json=update_payload, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Documento não encontrado."