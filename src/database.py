from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

DB_USER = os.getenv('POSTGRES_USER', 'user_example')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'example')
DB_DATABASE = os.getenv('POSTGRES_DB', 'db_example')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": DB_HOST,
                "port": DB_PORT,
                "user": DB_USER,
                "password": DB_PASS,
                "database": DB_DATABASE,
            },
        },
    },
    "apps": {
        "models": {
            "models": [
                "src.user.models", 
                "src.documents.models", 
                "src.transport.models", 
                "src.chatbot.models",
                "aerich.models"
            ], 
            "default_connection": "default",
        },
    },
}

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()

def init_tortoise(app):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    print("Tortoise ORM registrado!")
