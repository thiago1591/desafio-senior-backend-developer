from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from fastapi import Depends
from typing import Any
from .exceptions import InvalidCredentials
from src.config import auth_settings

http_bearer = HTTPBearer()


async def parse_jwt_data(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict[str, Any]:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=[auth_settings.JWT_ALG])
        return {"user_id": payload["id"]}
    except JWTError:
        raise InvalidCredentials()
