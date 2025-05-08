from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from fastapi import Depends
from . import service
from .exceptions import InvalidCredentials, UserNotOwner
from typing import Any
from src.config import auth_settings 

http_bearer = HTTPBearer()

async def parse_jwt_data(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict[str, Any]:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=[auth_settings.JWT_ALG])
        print(payload)
        return {"user_id": payload["user_id"]}
    except JWTError:
        raise InvalidCredentials()


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
