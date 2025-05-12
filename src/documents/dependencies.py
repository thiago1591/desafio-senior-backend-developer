from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends
from . import service
from .exceptions import InvalidCredentials, UserNotOwner
from typing import Any
from src.config import auth_settings 


async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()
    print(payload)
    return {"user_id": payload["user_id"]}


async def valid_document_id(document_id: int) -> dict[str, Any]:
    document = await service.get_document(document_id)  
    return document

async def valid_owned_document(
    document: dict[str, Any] = Depends(valid_document_id),
    token_data: dict[str, Any] = Depends(parse_jwt_data)
) -> dict[str, Any]:
    if document.user_id != token_data["user_id"]:
        raise UserNotOwner()
    return document
