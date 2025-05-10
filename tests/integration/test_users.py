import pytest
from httpx import AsyncClient
from datetime import date
from fastapi import status

from src.user.models import User

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_successfully(client: AsyncClient):
    user_payload = {
        "full_name": "João da Silva",
        "email": "joao.silva.miguel@example.com",
        "birth_date": "1990-05-20",
        "cpf": "30721764002",
        "phone": "11998765432",
        "password": "SenhaSegura123"
    }

    response = await client.post("/users/register", json=user_payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data["full_name"] == user_payload["full_name"]
    assert data["email"] == user_payload["email"]
    assert data["birth_date"] == user_payload["birth_date"]
    assert data["cpf"] == user_payload["cpf"]
    assert data["phone"] == user_payload["phone"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    
@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_with_invalid_credentials(client: AsyncClient):
    invalid_cpf_payload = {
        "full_name": "João da Silva",
        "email": "joao.silva.miguel@example.com",
        "birth_date": "1990-05-20",
        "cpf": "12345678901", 
        "phone": "11998765432",
        "password": "SenhaSegura123"
    }
    
    response = await client.post("/users/register", json=invalid_cpf_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "CPF inválido" in data["detail"][0]["msg"]

    invalid_phone_payload = {
        "full_name": "João da Silva",
        "email": "joao.silva.miguel@example.com",
        "birth_date": "1990-05-20",
        "cpf": "30721764002",
        "phone": "11999",  
        "password": "SenhaSegura123"
    }
    
    response = await client.post("/users/register", json=invalid_phone_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "Telefone deve conter apenas números (10 ou 11 dígitos)" in data["detail"][0]["msg"]

    short_password_payload = {
        "full_name": "João da Silva",
        "email": "joao.silva.miguel@example.com",
        "birth_date": "1990-05-20",
        "cpf": "30721764002",
        "phone": "11998765432",
        "password": "Senha"  
    }
    
    response = await client.post("/users/register", json=short_password_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "A senha deve ter pelo menos 8 caracteres" in data["detail"][0]["msg"]

    no_uppercase_password_payload = {
        "full_name": "João da Silva",
        "email": "joao.silva.miguel@example.com",
        "birth_date": "1990-05-20",
        "cpf": "30721764002",
        "phone": "11998765432",
        "password": "senhasegura123" 
    }
    
    response = await client.post("/users/register", json=no_uppercase_password_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "A senha deve conter pelo menos uma letra maiúscula" in data["detail"][0]["msg"]

    no_number_password_payload = {
        "full_name": "João da Silva",
        "email": "joao.silva.miguel@example.com",
        "birth_date": "1990-05-20",
        "cpf": "30721764002",
        "phone": "11998765432",
        "password": "SenhaSemNumero" 
    }
    
    response = await client.post("/users/register", json=no_number_password_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "A senha deve conter pelo menos um número" in data["detail"][0]["msg"]
    
@pytest.mark.anyio
@pytest.mark.integration
async def test_get_user_successfully(client: AsyncClient):
    user_payload = {
        "full_name": "Teste da Silva",
        "email": "teste.silva@example.com",
        "birth_date": "1990-05-20",
        "cpf": "48214669022",
        "phone": "11998765432",
        "password": "SenhaSegura123"
    }
    
    response = await client.post("/users/register", json=user_payload)
    assert response.status_code == 201  
    user_data = response.json()
    
    user_id = user_data["id"] 

    response = await client.get(f"/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["full_name"] == "Teste da Silva"
    assert data["email"] == "teste.silva@example.com"
    assert data["birth_date"] == "1990-05-20"
    assert data["cpf"] == "48214669022"
    assert data["phone"] == "11998765432"

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/users/9999") 
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Usuário não encontrado."
    
@pytest.mark.anyio
@pytest.mark.integration
async def test_get_users_successfully(client: AsyncClient):
    await User.all().delete()
    cpfs_validos = ["93416193008", "52833549032", "68068566082"]

    for i, cpf in enumerate(cpfs_validos):
        user_payload = {
            "full_name": f"Usuário Teste {i} da Silva",
            "email": f"usuarioo{i}@example.com",
            "birth_date": "1990-01-01",
            "cpf": cpf,
            "phone": f"1199999000{i}",
            "password": "SenhaSegura123"
        }
        response = await client.post("/users/register", json=user_payload)
        print(f"User {i} created with response: {response.json()}")
        assert response.status_code == status.HTTP_201_CREATED

    response = await client.get("/users/?skip=0&limit=10")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

    first_user = data[0]
    assert "id" in first_user
    assert "full_name" in first_user
    assert "email" in first_user
    assert "birth_date" in first_user
    assert "cpf" in first_user
    assert "phone" in first_user
    assert "created_at" in first_user
    assert "updated_at" in first_user

@pytest.mark.anyio
@pytest.mark.integration
async def test_update_user_successfully(client: AsyncClient):
    await User.all().delete()

    user_payload = {
        "full_name": "Usuário Original",
        "email": "original@example.com",
        "birth_date": "1990-01-01",
        "cpf": "93416193008",
        "phone": "11999990000",
        "password": "SenhaSegura123"
    }

    response = await client.post("/users/register", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    user_data = response.json()
    user_id = user_data["id"]

    update_payload = {
        "full_name": "Usuário Atualizado",
        "email": "atualizado@example.com",
        "birth_date": "1991-02-02",
        "cpf": "52833549032",
        "phone": "11988880000"
    }

    response = await client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK

    updated_user = response.json()
    assert updated_user["id"] == user_id
    assert updated_user["full_name"] == update_payload["full_name"]
    assert updated_user["email"] == update_payload["email"]
    assert updated_user["birth_date"] == update_payload["birth_date"]
    assert updated_user["cpf"] == update_payload["cpf"]
    assert updated_user["phone"] == update_payload["phone"]
    assert updated_user["created_at"] != ""
    assert updated_user["updated_at"] != ""

@pytest.mark.anyio
@pytest.mark.integration
async def test_delete_user_successfully(client: AsyncClient):
    await User.all().delete()

    user_payload = {
        "full_name": "Usuário para Deletar",
        "email": "deletar@example.com",
        "birth_date": "1990-01-01",
        "cpf": "68068566082",
        "phone": "11999990001",
        "password": "SenhaSegura123"
    }

    response = await client.post("/users/register", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    user_id = response.json()["id"]

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
