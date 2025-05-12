from typing import Any
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_404_NOT_FOUND
from src.transport.models import TransportCard
from jose import JWTError, jwt
from fastapi import Depends
from .exceptions import InvalidCredentials
from src.config import auth_settings 

async def get_card_by_number_or_404(card_number: str) -> TransportCard:
    card = await TransportCard.get_or_none(card_number=card_number)
    if not card:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cartão de transporte não encontrado")
    return card

async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["user_id"]}