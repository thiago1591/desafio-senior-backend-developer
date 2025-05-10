import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from src.main import app

test_user = {"username": "test", "password": "test"}

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        print('vai criar o bd')
        await Tortoise.init(
            db_url="sqlite://:memory:",
            modules={"models": [
                "src.user.models", 
                "src.documents.models", 
                "src.transport.models", 
                "src.chatbot.models",
            ]},
        )
        await Tortoise.generate_schemas()

        #await sample_seeders.generate_seeders(number_of_users=1, test_user=test_user)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c

        await Tortoise.close_connections() 
