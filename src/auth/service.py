from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from src.user.models import User
from .schemas import UserLoginResponse, UserAuthenticated, UserSignup, UserLogin
from .exceptions import InvalidCredentials
from src.config import auth_settings  # Importando as configurações
import os

# Instanciando o passlib para criptografar senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar um token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=auth_settings.JWT_EXP)  # Usando a configuração de expiração
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG)  # Usando a chave e algoritmo configurados
    return encoded_jwt

# Função para verificar a senha (comparando com a hash armazenada)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar a hash da senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Serviço para login
async def authenticate_user(username: str, password: str):
    user = await User.filter(username=username).first()
    if user is None or not verify_password(password, user.password):
        raise InvalidCredentials(detail="Usuário ou senha inválidos.")
    return user

async def login_user(user_login: UserLogin):
    user = await authenticate_user(user_login.username, user_login.password)
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    return UserLoginResponse(access_token=access_token, user_id=user.id, username=user.username)
