import pytest
from fastapi import status
from httpx import AsyncClient


class TestSaldoWsLidRoutes:
    @pytest.mark.parametrize(
        "in_format",
        [
            "json",
            "xml",
            "html",
        ],
    )
    @pytest.mark.asyncio
    async def test_invalid_input_returns_422(
        self, client: AsyncClient, in_format: str
    ) -> None:
        res = await client.get(f"/saldo-ws/lid/{in_format}/bad-input")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "lid",
        [
            "dväljas..vb.1",
        ],
    )
    @pytest.mark.parametrize(
        "in_format, expected_content_type",
        [
            ("json", "application/json"),
            ("xml", "application/xml"),
            ("html", "text/html; charset=utf-8"),
        ],
    )
    @pytest.mark.asyncio
    async def test_valid_input_returns_200(
        self,
        client: AsyncClient,
        in_format: str,
        expected_content_type: str,
        lid: str,
    ) -> None:
        res = await client.get(f"/saldo-ws/lid/{in_format}/{lid}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == expected_content_type
