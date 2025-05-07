from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

class InvalidCredentials(HTTPException):
    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=detail)

class UserNotFound(HTTPException):
    def __init__(self, detail: str = "Usuário não encontrado"):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)
