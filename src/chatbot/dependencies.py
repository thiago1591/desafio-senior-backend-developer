from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends
from typing import Any
from .exceptions import InvalidCredentials
from src.config import auth_settings 

async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["user_id"]}
