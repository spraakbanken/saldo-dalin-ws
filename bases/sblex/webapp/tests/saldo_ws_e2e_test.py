import pytest

from fastapi import status
from httpx import AsyncClient


class TestSaldoWsMd1Routes:
    @pytest.mark.parametrize("in_format", ["json","xml","html",])
    @pytest.mark.asyncio
    async def test_invalid_input_returns_422(self, client: AsyncClient, in_format: str):
        res = await client.get(f"/saldo-ws/md1/{in_format}/bad-input")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
