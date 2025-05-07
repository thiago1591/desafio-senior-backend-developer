# dependencies.py

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from . import service
from .exceptions import DocumentNotFound, InvalidCredentials, UserNotOwner
from typing import Any
from pydantic import UUID4  # Se usar UUID; senão, use int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
JWT_SECRET = "JWT_SECRET"  # Idealmente: use uma variável de ambiente

async def parse_jwt_data(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return {"user_id": payload["id"]}
    except JWTError:
        raise InvalidCredentials()


async def valid_document_id(document_id: int) -> dict[str, Any]:
    document = await service.get_document_raw(document_id)  # nova função que retorna o model direto
    if not document:
        raise DocumentNotFound()
    return document


async def valid_owned_document(
    document: dict[str, Any] = Depends(valid_document_id),
    token_data: dict[str, Any] = Depends(parse_jwt_data)
) -> dict[str, Any]:
    if document.user_id != token_data["user_id"]:
        raise UserNotOwner()
    return document
