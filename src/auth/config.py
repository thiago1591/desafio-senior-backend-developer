from datetime import timedelta
from pydantic_settings import BaseSettings

class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"  # Algoritmo de assinatura do JWT
    JWT_SECRET: str  # A chave secreta para gerar o JWT
    JWT_EXP: int = 5  # Expiração do token em minutos
    REFRESH_TOKEN_KEY: str  # Chave secreta para gerar o refresh token
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)  # Expiração do refresh token
    SECURE_COOKIES: bool = True  # Se os cookies de autenticação serão seguros

# Instancia a configuração para ser usada em outros lugares
auth_settings = AuthConfig()
