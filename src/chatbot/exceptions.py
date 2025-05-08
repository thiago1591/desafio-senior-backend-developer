from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

class InvalidCredentials(HTTPException):
    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=detail)