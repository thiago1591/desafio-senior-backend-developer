from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Schema para Login do Usuário
class UserLogin(BaseModel):
    username: str
    password: str

# Resposta de Login (inclui o token JWT e informações do usuário)
class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

# Informações do Usuário após autenticação
class UserAuthenticated(BaseModel):
    id: int
    username: str
    email: str
    birth_date: Optional[str] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

# Para Cadastro de Novo Usuário
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    birth_date: Optional[date] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None
