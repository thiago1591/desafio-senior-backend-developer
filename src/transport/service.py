from tortoise.transactions import in_transaction
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
import secrets

from .models import TransportCard, TransportTransactionHistory
from .schemas import RechargeRequest
from ..documents.exceptions import UserNotOwner

async def recharge_card(card_number: str, amount: int, user_id: str):

    try:
        card = await TransportCard.get_or_none(card_number=card_number)
        if not card:
            raise HTTPException(status_code=404, detail="Cartão não encontrado")

        if card.user_id != user_id:
            raise UserNotOwner()

        card.balance += amount
        await card.save()

        await TransportTransactionHistory.create(
            card=card,
            amount=amount,
            type="recharge"
        )

        return {
            "card_number": card.card_number,
            "new_balance": card.balance
        }

    except HTTPException as e:
        raise e  
    
    except Exception as e:
        print(f"Erro durante o processo de recarga para o cartão {card_number}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

async def debit_card(card: TransportCard, amount: int):
    card.balance -= amount
    await card.save()

    await TransportTransactionHistory.create(
        card=card,
        type="debit",
        amount=amount
    )

    return card

async def get_transaction_history(card):
    transactions = await TransportTransactionHistory.filter(card=card).all()
    
    return [
        {
            "id": transaction.id,
            "card_number": card.card_number,
            "transaction_type": transaction.type,
            "amount": transaction.amount,
            "balance_after_transaction": card.balance, 
            "transaction_date": transaction.created_at
        } for transaction in transactions
    ]

async def get_user_cards(user_id: int):
    cards = await TransportCard.filter(user_id=user_id).all()
    
    if not cards:
        return []
    
    return cards

async def create_transport_card(user_id: int) -> TransportCard:
    #tenta gerar um código único de cartão até achar um que é único
    while True:
        card_number = ''.join(secrets.choice('0123456789') for _ in range(16))
        existing_card = await TransportCard.get_or_none(card_number=card_number)
        if not existing_card:
            break
    
    card = await TransportCard.create(
        user_id=user_id,
        card_number=card_number,
        balance=0.00,
        status='active'
    )
    
    return card