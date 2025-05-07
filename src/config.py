
from pydantic_settings import BaseSettings  
from datetime import timedelta

class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"  
    JWT_SECRET: str 
    JWT_EXP: int = 5  
    
    REFRESH_TOKEN_KEY: str 
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30) 
    
    SECURE_COOKIES: bool = True  

    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"
        extra = "allow"

auth_settings = AuthConfig()
