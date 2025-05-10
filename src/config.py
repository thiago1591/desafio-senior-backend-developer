from pydantic_settings import BaseSettings
from datetime import timedelta
class AppSettings(BaseSettings):
    TESTING: bool = False
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutos

    REFRESH_TOKEN_KEY: str
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)

    SECURE_COOKIES: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = AppSettings()
auth_settings = AuthConfig()
