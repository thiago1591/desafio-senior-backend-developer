from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

class UserNotOwner(HTTPException):
    def __init__(self, detail: str = "Usuário não é o proprietário do recurso"):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)

class InvalidCredentials(HTTPException):
    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=detail)