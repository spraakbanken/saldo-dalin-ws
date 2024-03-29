from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import HTMLResponse
from sblex.schemas import Lexeme
from sblex.webapp.responses import XMLResponse

router = APIRouter()


@router.get("/json/{arg}")
async def calculate_md1_json(
    arg: Lexeme,
):
    xs = [
        arg,
    ]

    return xs


@router.get(
    "/xml/{arg}",
    response_class=XMLResponse,
)
async def calculate_md1_xml(
    arg: Lexeme,
):
    xs = [
        arg,
    ]

    return xmlize(xs)


@router.get(
    "/html/{arg}",
    response_class=HTMLResponse,
)
async def calculate_md1_html(
    arg: Lexeme,
):
    xs = [
        arg,
    ]

    return f"{xs}"


def xmlize(xs: list) -> bytes:
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    for x in xs:
        xml += "<l>" + x + "</l>\n"
    xml += "</result>\n"
    return xml.encode("utf-8")
