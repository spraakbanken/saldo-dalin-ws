from fastapi import status
from httpx import AsyncClient


class TestSaldoWsMd1Routes:
    @pytest.mark.asyncio
    async def test_invalid_input_returns_422(self, client: AsyncClient):
        res = await client.get("/saldo-ws/md1/json/bad-input")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
