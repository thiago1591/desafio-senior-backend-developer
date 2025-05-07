from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.transport import schemas, service
from src.transport.dependencies import get_card_by_number_or_404
from src.documents.exceptions import UserNotOwner
from .dependencies import parse_jwt_data

router = APIRouter(prefix="/transport-card", tags=["transport-card"])

@router.get("/{card_number}/balance", response_model=schemas.TransportCardResponse)
async def get_balance(
    card_number: str,
    token_data: dict = Depends(parse_jwt_data),
    card = Depends(get_card_by_number_or_404)
):
    if card.user_id != token_data["user_id"]:
        raise UserNotOwner()
    return card

@router.post("/{card_number}/recharge", response_model=schemas.TransportCardResponse)
async def recharge_card(
    card_number: str,
    payload: schemas.TransportCardRecharge,
    token_data: dict = Depends(parse_jwt_data),
    card = Depends(get_card_by_number_or_404)
):
    if card.user_id != token_data["user_id"]:
        raise UserNotOwner()
    return await service.recharge_card(card, payload.amount)

@router.post("/{card_number}/debit", response_model=schemas.TransportCardResponse)
async def debit_card(
    card_number: str,
    payload: schemas.TransportCardDebit,
    token_data: dict = Depends(parse_jwt_data),
    card = Depends(get_card_by_number_or_404)
):
    if card.user_id != token_data["user_id"]:
        raise UserNotOwner()
    
    if card.balance < payload.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente para realizar o débito"
        )

    updated_card = await service.debit_card(card, payload.amount)
    return updated_card

@router.get("/{card_number}/history", response_model=List[schemas.TransportTransactionHistoryResponse])
async def get_transaction_history(
    card_number: str,
    token_data: dict = Depends(parse_jwt_data),
    card = Depends(get_card_by_number_or_404)
):
    if card.user_id != token_data["user_id"]:
        raise UserNotOwner()
    
    history = await service.get_transaction_history(card)
    return history
