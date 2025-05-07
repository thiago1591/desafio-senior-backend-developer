from pydantic import BaseModel, EmailStr
from typing import Optional

from datetime import date

class UserBase(BaseModel):
    username: str
    email: EmailStr
    birth_date: Optional[date] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    birth_date: Optional[date] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True
