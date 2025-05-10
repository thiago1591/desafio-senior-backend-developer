import pytest
from httpx import AsyncClient
from fastapi import status
from src.user.models import User

@pytest.mark.anyio
@pytest.mark.integration
async def test_login_successfully(client: AsyncClient):
    await User.all().delete()

    user_payload = {
        "full_name": "Usuário Teste",
        "email": "usuario.test@example.com",
        "birth_date": "1990-01-01",
        "cpf": "14781951775",
        "phone": "11999990000",
        "password": "SenhaSegura123"
    }

    response = await client.post("/users/register", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED

    login_payload = {
        "cpf": user_payload["cpf"],
        "password": user_payload["password"]
    }

    login_response = await client.post("/auth/login", json=login_payload)

    assert login_response.status_code == status.HTTP_200_OK

    login_data = login_response.json()

    token = login_data.get("access_token")
    assert token is not None, "Token não encontrado na resposta de login"
    
    assert isinstance(token, str) and len(token) > 0, "Token inválido"

@pytest.mark.anyio
@pytest.mark.integration
async def test_login_with_incorrect_credentials(client: AsyncClient):
    await User.all().delete()

    user_payload = {
        "full_name": "Usuário Teste",
        "email": "usuario.test@example.com",
        "birth_date": "1990-01-01",
        "cpf": "14781951775",
        "phone": "11999990000",
        "password": "SenhaSegura123"
    }
    
    response = await client.post("/users/register", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED

    invalid_cpf_payload = {
        "cpf": "12345678901", 
        "password": user_payload["password"]
    }
    login_response = await client.post("/auth/login", json=invalid_cpf_payload)
    assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    login_data = login_response.json()
    assert "detail" in login_data
    assert "CPF inválido" in login_data["detail"][0]["msg"]

    invalid_password_payload = {
        "cpf": user_payload["cpf"],
        "password": "senha"  
    }
    login_response = await client.post("/auth/login", json=invalid_password_payload)
    assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    login_data = login_response.json()
    assert "detail" in login_data
    assert "A senha deve ter pelo menos 8 caracteres" in login_data["detail"][0]["msg"]

    invalid_password_payload = {
        "cpf": user_payload["cpf"],
        "password": "senha123" 
    }
    login_response = await client.post("/auth/login", json=invalid_password_payload)
    assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    login_data = login_response.json()
    assert "detail" in login_data
    assert "A senha deve conter pelo menos uma letra maiúscula" in login_data["detail"][0]["msg"]

    invalid_password_payload = {
        "cpf": user_payload["cpf"],
        "password": "SenhaSemNumero" 
    }
    login_response = await client.post("/auth/login", json=invalid_password_payload)
    assert login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    login_data = login_response.json()
    assert "detail" in login_data
    assert "A senha deve conter pelo menos um número" in login_data["detail"][0]["msg"]

    incorrect_password_payload = {
        "cpf": user_payload["cpf"],
        "password": "SenhaErrada123"  
    }
    login_response = await client.post("/auth/login", json=incorrect_password_payload)
    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
    login_data = login_response.json()
    assert "detail" in login_data
    assert "CPF ou senha inválidos" in login_data["detail"] 