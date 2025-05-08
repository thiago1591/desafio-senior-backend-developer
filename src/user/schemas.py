from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date
import re
from src.user.utils import is_valid_cpf

class UserBase(BaseModel):
    full_name: str = Field(..., example="João da Silva")
    email: EmailStr = Field(..., example="joao.silva@example.com")
    birth_date: date = Field(..., example="1990-05-20")
    cpf: str = Field(..., example="12345678909")
    phone: str = Field(..., example="11998765432") 

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if len(v.strip().split()) < 2:
            raise ValueError('O nome completo deve conter pelo menos nome e sobrenome.')
        return v

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v):
        if not is_valid_cpf(v):
            raise ValueError('CPF inválido.')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.fullmatch(r'\d{10,11}', v):
            raise ValueError('Telefone deve conter apenas números (10 ou 11 dígitos).')
        return v

class UserCreate(UserBase):
    password: str = Field(..., example="senhaSegura123")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres.')
        if not re.search(r'[A-Z]', v):  
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[0-9]', v):
            raise ValueError('A senha deve conter pelo menos um número.')
        return v

class UserUpdate(BaseModel):
    full_name: str = Field(..., example="João da Silva")
    email: EmailStr = Field(..., example="joao.silva@example.com")
    birth_date: date = Field(..., example="1990-05-20")
    cpf: str = Field(..., example="12345678909")
    phone: str = Field(..., example="11998765432")

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if len(v.strip().split()) < 2:
            raise ValueError('O nome completo deve conter pelo menos nome e sobrenome.')
        return v

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v):
        if not is_valid_cpf(v):
            raise ValueError('CPF inválido.')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.fullmatch(r'\d{10,11}', v):
            raise ValueError('Telefone deve conter apenas números (10 ou 11 dígitos).')
        return v

class UserResponse(UserBase):
    id: int = Field(..., example=1)
    created_at: str = Field(..., example="2024-01-01T12:00:00")
    updated_at: str = Field(..., example="2024-01-10T08:30:00")

    class Config:
        orm_mode = True
