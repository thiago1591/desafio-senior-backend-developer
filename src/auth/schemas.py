import re
from pydantic import BaseModel, field_validator, Field
from src.auth.utils import is_valid_cpf 

class UserLogin(BaseModel):
    username: str = Field(..., example="12345678909")
    password: str = Field(..., example="senhaSegura123")

    @field_validator('username')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        if not is_valid_cpf(v):
            raise ValueError('CPF inválido.')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[0-9]', v):
            raise ValueError('A senha deve conter pelo menos um número.')
        return v

class UserLoginResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")
    user_id: int = Field(..., example=1)
    cpf: str = Field(..., example="77042986075")
