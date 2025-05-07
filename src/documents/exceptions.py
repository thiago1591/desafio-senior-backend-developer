from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

class DocumentNotFound(HTTPException):
    def __init__(self, detail: str = "Documento não encontrado"):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)

class InvalidCredentials(HTTPException):
    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=detail)

class UserNotOwner(HTTPException):
    def __init__(self, detail: str = "Usuário não é o proprietário do documento"):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)