from fastapi import HTTPException
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.user.service import create_user, delete_user, get_users, update_user
from src.user.schemas import UserCreate, UserResponse, UserUpdate

@pytest.mark.asyncio
@patch("src.user.service.create_transport_card", new_callable=AsyncMock)
@patch("src.user.service.User.create", new_callable=AsyncMock)
@patch("src.user.service.User.filter")
async def test_create_user_success(mock_filter, mock_create, mock_create_card):
    mock_filter.return_value.exists = AsyncMock(side_effect=[False, False])

    mock_user_instance = MagicMock()
    mock_user_instance.id = 1
    mock_user_instance.full_name = "João da Silva"
    mock_user_instance.email = "joao@example.com"
    mock_user_instance.birth_date = "1990-01-01"
    mock_user_instance.cpf = "14781951775"
    mock_user_instance.phone = "11999999999"
    mock_user_instance.created_at = None
    mock_user_instance.updated_at = None

    mock_create.return_value = mock_user_instance

    user_create = UserCreate(
        full_name="João da Silva",
        email="joao@example.com",
        password="Teste123",
        birth_date="1990-01-01",
        cpf="14781951775",
        phone="11999999999"
    )

    result = await create_user(user_create)

    assert isinstance(result, UserResponse)
    assert result.full_name == "João da Silva"
    mock_create_card.assert_awaited_once_with(1)
    
@pytest.mark.asyncio
@patch("src.user.service.User.filter")
async def test_create_user_fails_when_cpf_exists(mock_filter):
    mock_filter.return_value.exists = AsyncMock(side_effect=[True])  

    user_create = UserCreate(
        full_name="João da Silva",
        email="joao@example.com",
        password="Teste123",
        birth_date="1990-01-01",
        cpf="14781951775",
        phone="11999999999"
    )

    with pytest.raises(HTTPException) as exc_info:
        await create_user(user_create)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "CPF ou e-mail já cadastrado."

@pytest.mark.asyncio
@patch("src.user.service.User.filter")
async def test_create_user_fails_when_email_exists(mock_filter):
    mock_filter.return_value.exists = AsyncMock(side_effect=[False, True])

    user_create = UserCreate(
        full_name="Maria Oliveira",
        email="maria@example.com",
        password="Senha123",
        birth_date="1985-05-20",
        cpf="14781951775",
        phone="11988887777"
    )

    with pytest.raises(HTTPException) as exc_info:
        await create_user(user_create)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "CPF ou e-mail já cadastrado."


@pytest.mark.asyncio
@patch("src.user.service.create_transport_card", new_callable=AsyncMock)
@patch("src.user.service.User.create", new_callable=AsyncMock)
@patch("src.user.service.User.filter")
async def test_password_not_in_user_response(mock_filter, mock_create, mock_create_card):
    mock_filter.return_value.exists = AsyncMock(side_effect=[False, False])

    mock_user_instance = MagicMock()
    mock_user_instance.id = 1
    mock_user_instance.full_name = "João da Silva"
    mock_user_instance.email = "joao@example.com"
    mock_user_instance.birth_date = "1990-01-01"
    mock_user_instance.cpf = "14781951775"
    mock_user_instance.phone = "11999999999"
    mock_user_instance.created_at = None
    mock_user_instance.updated_at = None
    mock_user_instance.password = "senha_criptografada"

    mock_create.return_value = mock_user_instance

    user_create = UserCreate(
        full_name="João da Silva",
        email="joao@example.com",
        password="Teste123",
        birth_date="1990-01-01",
        cpf="14781951775",
        phone="11999999999"
    )

    result = await create_user(user_create)

    assert isinstance(result, UserResponse)
    assert not hasattr(result, "password"), "A resposta não deve conter o campo 'password'"
    
@pytest.mark.asyncio
@patch("src.user.service.User.all")
#testa se a paginaçao está funcionando. Isso é importante para
#garantir que não faça uma busca em todos os usuários
async def test_get_users_pagination_applied(mock_all):
    mock_query = MagicMock()
    mock_all.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit = AsyncMock(return_value=[])

    skip = 5
    limit = 20

    result = await get_users(skip=skip, limit=limit)

    mock_query.offset.assert_called_once_with(skip)
    mock_query.limit.assert_awaited_once_with(limit)

    assert result == []
    
@pytest.mark.asyncio
@patch("src.user.service.User.filter")
async def test_update_user_success(mock_filter):
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.full_name = "Nome Antigo"
    mock_user.email = "antigo@example.com"
    mock_user.birth_date = "1990-01-01"
    mock_user.cpf = "12345678900"
    mock_user.phone = "11999999999"
    mock_user.created_at = None
    mock_user.updated_at = None
    mock_user.save = AsyncMock()

    mock_filter.return_value.first = AsyncMock(return_value=mock_user)

    update_data = UserUpdate(
        full_name="Novo Nome", 
        email="antigo@example.com", 
        birth_date="1990-01-01", 
        cpf="14781951775", 
        phone="11999999999"
    )

    response = await update_user(1, update_data)

    assert isinstance(response, UserResponse)
    assert response.full_name == "Novo Nome"
    mock_user.save.assert_awaited_once()
    
@pytest.mark.asyncio
@patch("src.user.service.User.filter")
async def test_delete_user_success(mock_filter):
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.full_name = "João da Silva"
    mock_user.email = "joao@example.com"
    mock_user.birth_date = "1990-01-01"
    mock_user.cpf = "14781951775"
    mock_user.phone = "11999999999"
    mock_user.created_at = None
    mock_user.updated_at = None
    mock_user.delete = AsyncMock()

    mock_filter.return_value.first = AsyncMock(return_value=mock_user)

    response = await delete_user(1)

    assert response == {"detail": "Usuário excluído com sucesso."}
    mock_user.delete.assert_awaited_once()