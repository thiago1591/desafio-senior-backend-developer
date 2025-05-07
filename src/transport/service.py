from tortoise.transactions import in_transaction
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from .models import TransportCard, TransportTransactionHistory
from .schemas import RechargeRequest
from ..documents.exceptions import UserNotOwner


async def recharge_card(card_number: str, data: RechargeRequest, token_data: dict):
    card = await TransportCard.get_or_none(card_number=card_number)

    if not card:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cartão não encontrado")

    if card.user_id != token_data["user_id"]:
        raise UserNotOwner()

    async with in_transaction():
        card.balance += data.amount
        await card.save()

        await TransportTransactionHistory.create(
            card=card,
            amount=data.amount,
            type="recharge"
        )

    return {
        "card_number": card.card_number,
        "new_balance": card.balance
    }

async def debit_card(card: TransportCard, amount: int):
    card.balance -= amount
    await card.save()

    transaction = TransportTransactionHistory(
        card=card,
        type="debit",
        amount=amount
    )
    await transaction.save()

    return card

async def get_transaction_history(card):
    return await TransportTransactionHistory.filter(card=card).all()