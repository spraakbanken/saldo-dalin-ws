import pytest
from fastapi import status
from httpx import AsyncClient


class TestSaldoWsFLRoutes:
    @pytest.mark.parametrize(
        "segment, expected_response",
        [
            ("t", []),
            (
                "dväljs",
                [
                    {
                        "id": "dväljas..1",
                        "fm": "bo..1",
                        "fp": "PRIM..1",
                        "l": "dväljas..vb.1",
                        "gf": "dväljas",
                        "p": "vb_vs_dväljas",
                    }
                ],
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_json_valid_input_returns_200(
        self,
        client: AsyncClient,
        segment: str,
        expected_response: list,
    ) -> None:
        res = await client.get(f"/saldo-ws/fl/json/{segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/json"

        assert res.json() == expected_response

    @pytest.mark.parametrize(
        "segment, expected_response",
        [
            ("t", '<?xml version="1.0" encoding="UTF-8"?>\n<result>\n\n</result>'),
            (
                "dväljs",
                '<?xml version="1.0" encoding="UTF-8"?>\n<result>\n\n    <a><id>dväljas..1</id><fm>bo..1</fm><fp>PRIM..1</fp><l>dväljas..vb.1</l><gf>dväljas</gf><p>vb_vs_dväljas</p></a>\n\n</result>',
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_xml_valid_input_returns_200(
        self,
        client: AsyncClient,
        segment: str,
        expected_response: str,
    ) -> None:
        res = await client.get(f"/saldo-ws/fl/xml/{segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "application/xml"

        assert res.text == expected_response

    @pytest.mark.parametrize(
        "segment, expected_in_response",
        [("", "Mata in en ordform."), ("dväljs", "dväljs"),("dväljsxdf", "ordet saknas i lexikonet")],
    )
    @pytest.mark.asyncio
    async def test_html_valid_input_returns_200(
        self,
        client: AsyncClient,
        segment: str,
        expected_in_response: str,
    ) -> None:
        res = await client.get(f"/saldo-ws/fl/html/{segment}")
        assert res.status_code == status.HTTP_200_OK
        assert res.headers["content-type"] == "text/html; charset=utf-8"

        assert expected_in_response in res.text
