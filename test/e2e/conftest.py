from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sblex.webapp.main import create_app


@pytest.fixture(name="app")
def fixture_app() -> FastAPI:
    return create_app(
        config={
            "SALDO_MORPHOLOGY_PATH": "assets/testing/saldo.lex",
            "SALDO_SEMANTIC_PATH": "assets/testing/saldo.txt",
        }
    )


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client
