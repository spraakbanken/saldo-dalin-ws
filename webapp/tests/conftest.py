import pytest
import pytest_asyncio

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from webapp.main import create_app


@pytest.fixture(name="app")
def fixture_app() -> FastAPI:
    return create_app()
    
@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver"
        ) as client:
            yield client