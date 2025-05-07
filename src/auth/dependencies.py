from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Any
from src.auth.exceptions import InvalidCredentials
from src.config import auth_settings  

http_bearer = HTTPBearer()

async def parse_jwt_data(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict[str, Any]:
    token = credentials.credentials  
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=[auth_settings.JWT_ALG])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["id"]}


