from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from src.transport.service import recharge_card


@pytest.mark.asyncio
@patch("src.transport.models.TransportTransactionHistory.create", new_callable=AsyncMock)
@patch("src.transport.models.TransportCard.get_or_none", new_callable=AsyncMock)
async def test_recharge_card_success(
    mock_get_card,
    mock_create_transaction,
):
    mock_card = MagicMock()
    mock_card.card_number = "1234567890123456"
    mock_card.user_id = 1
    mock_card.balance = 1000 
    mock_card.save = AsyncMock() 
    mock_get_card.return_value = mock_card 

    mock_create_transaction.return_value = MagicMock()

    result = await recharge_card("1234567890123456", 500, 1)

    assert result["card_number"] == "1234567890123456"
    assert result["new_balance"] == 1500  
    mock_get_card.assert_awaited_once()
    mock_card.save.assert_awaited_once()
    mock_create_transaction.assert_awaited_once()

@pytest.mark.asyncio
@patch("src.transport.models.TransportCard.get_or_none", new_callable=AsyncMock)
async def test_recharge_card_card_not_found(mock_get_card):
    mock_get_card.return_value = None

    with pytest.raises(Exception) as exc_info:
        await recharge_card("0000000000000000", 500, 1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Cartão não encontrado"
    mock_get_card.assert_awaited_once()

@pytest.mark.asyncio
@patch("src.transport.models.TransportTransactionHistory.create", new_callable=AsyncMock)
@patch("src.transport.models.TransportCard.get_or_none", new_callable=AsyncMock)
async def test_multiple_recharges_accumulates_correctly(
    mock_get_card,
    mock_create_transaction,
):
    mock_card = MagicMock()
    mock_card.card_number = "1234567890123456"
    mock_card.user_id = 1
    mock_card.balance = 0
    mock_card.save = AsyncMock()

    mock_get_card.return_value = mock_card
    mock_create_transaction.return_value = MagicMock()

    result1 = await recharge_card("1234567890123456", 200, 1)
    assert result1["new_balance"] == 200

    result2 = await recharge_card("1234567890123456", 300, 1)
    assert result2["new_balance"] == 500

    result3 = await recharge_card("1234567890123456", 50, 1)
    assert result3["new_balance"] == 550

    assert mock_card.save.await_count == 3
    assert mock_create_transaction.await_count == 3

@pytest.mark.asyncio
@patch("src.transport.models.TransportTransactionHistory.create", new_callable=AsyncMock)
@patch("src.transport.models.TransportCard.get_or_none", new_callable=AsyncMock)
async def test_recharge_card_high_value(
    mock_get_card,
    mock_create_transaction,
):
    mock_card = MagicMock()
    mock_card.card_number = "1234567890123456"
    mock_card.user_id = 1
    mock_card.balance = 1000  
    mock_card.save = AsyncMock()  
    mock_get_card.return_value = mock_card 

    mock_create_transaction.return_value = MagicMock()

    amount = 1000000

    result = await recharge_card("1234567890123456", amount, 1)

    assert result["card_number"] == "1234567890123456"
    assert result["new_balance"] == 1001000  
    
    mock_get_card.assert_awaited_once()
    mock_card.save.assert_awaited_once()
    mock_create_transaction.assert_awaited_once()
    
from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from src.transport.service import debit_card


@pytest.mark.asyncio
@patch("src.transport.service.TransportTransactionHistory.create", new_callable=AsyncMock)
async def test_debit_card_success(mock_create_transaction):
    mock_card = MagicMock()
    mock_card.balance = 1000
    mock_card.save = AsyncMock()

    updated_card = await debit_card(mock_card, 300)

    assert updated_card.balance == 700  # 1000 - 300
    mock_card.save.assert_awaited_once()
    mock_create_transaction.assert_awaited_once_with(
        card=mock_card,
        type="debit",
        amount=300
    )
