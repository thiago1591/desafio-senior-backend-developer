from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from src.user.models import User
from .schemas import UserLoginResponse, UserLogin
from .exceptions import InvalidCredentials
from src.config import auth_settings  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=auth_settings.JWT_EXP)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def authenticate_user(cpf: str, password: str):
    user = await User.filter(cpf=cpf).first()
    if user is None or not verify_password(password, user.password):
        raise InvalidCredentials(detail="CPF ou senha inválidos.")
    return user

async def login_user(user_login: UserLogin):
    user = await authenticate_user(user_login.username, user_login.password)
    access_token = create_access_token(data={"sub": user.cpf, "user_id": user.id})
    return UserLoginResponse(access_token=access_token, user_id=user.id, cpf=user.cpf)
