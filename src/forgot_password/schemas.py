import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., example="usuario@email.com")


class VerifyCodeRequest(BaseModel):
    email: EmailStr = Field(..., example="usuario@email.com")
    code: str = Field(..., example="12345", min_length=5, max_length=5)


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(..., example="NovaSenha123")

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[0-9]', v):
            raise ValueError('A senha deve conter pelo menos um número.')
        return v
