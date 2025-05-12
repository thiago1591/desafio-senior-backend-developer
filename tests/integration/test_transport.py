from httpx import AsyncClient
import pytest
from fastapi import status

from src.transport.models import TransportCard
from src.user.models import User

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_user_cards_successfully(client: AsyncClient):
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
    user_data = response.json()

    login_response = await client.post("/auth/login", data={
        "username": user_payload["cpf"],
        "password": user_payload["password"]
    })
    assert login_response.status_code == status.HTTP_200_OK
    login_data = login_response.json()

    token = login_data.get("access_token")
    assert token is not None

    response = await client.get("/transport-card/my-cards", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    card = data[0]
    assert "id" in card
    assert "user_id" in card
    assert card["user_id"] == user_data["id"]
    assert "balance" in card
    assert "card_number" in card
    assert card["status"] == "active"

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_card_balance_successfully(client: AsyncClient):
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

    login_response = await client.post("/auth/login", data={
        "username": user_payload["cpf"],
        "password": user_payload["password"]
    })
    assert login_response.status_code == status.HTTP_200_OK
    login_data = login_response.json()

    token = login_data.get("access_token")
    assert token is not None
    assert isinstance(token, str) and len(token) > 0

    response = await client.get(
        "/transport-card/my-cards",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    card = data[0]
    card_number = card["card_number"]

    response = await client.get(
        f"/transport-card/{card_number}/balance",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    balance = response.json()
    assert isinstance(balance, int)
    assert balance == card["balance"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_recharge_card_successfully(client: AsyncClient):
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

    login_response = await client.post("/auth/login", data={
        "username": user_payload["cpf"],
        "password": user_payload["password"]
    })
    assert login_response.status_code == status.HTTP_200_OK
    login_data = login_response.json()

    token = login_data.get("access_token")
    assert token is not None
    assert isinstance(token, str) and len(token) > 0

    response = await client.get(
        "/transport-card/my-cards",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    card = data[0]
    card_number = card["card_number"]
    current_balance = card["balance"]

    recharge_payload = {
        "amount": 100
    }

    response = await client.post(
        f"/transport-card/{card_number}/recharge",
        json=recharge_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    recharge_data = response.json()

    assert "card_number" in recharge_data
    assert recharge_data["card_number"] == card_number
    assert "new_balance" in recharge_data
    assert recharge_data["new_balance"] == current_balance + recharge_payload["amount"]

    response = await client.get(
        f"/transport-card/{card_number}/balance",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    balance = response.json()
    assert balance == current_balance + recharge_payload["amount"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_debit_card_successfully(client: AsyncClient):
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

    login_response = await client.post("/auth/login", data={
        "username": user_payload["cpf"],
        "password": user_payload["password"]
    })
    assert login_response.status_code == status.HTTP_200_OK
    login_data = login_response.json()

    token = login_data.get("access_token")
    assert token is not None, "Token não encontrado na resposta de login"

    response = await client.get(
        "/transport-card/my-cards",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    card = data[0]
    card_number = card["card_number"]
    current_balance = card["balance"]

    debit_payload = {
        "amount": 100
    }

    response = await client.post(
        f"/transport-card/{card_number}/debit",
        json=debit_payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    if current_balance >= debit_payload["amount"]:
        assert response.status_code == status.HTTP_200_OK
        debit_data = response.json()

        assert "card_number" in debit_data
        assert debit_data["card_number"] == card_number
        assert "balance" in debit_data
        assert debit_data["balance"] == current_balance - debit_payload["amount"]

        response = await client.get(
            f"/transport-card/{card_number}/balance",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        balance = response.json()
        assert balance == current_balance - debit_payload["amount"]
    else:
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_data = response.json()
        assert error_data["detail"] == "Saldo insuficiente para realizar o débito"
