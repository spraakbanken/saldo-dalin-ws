from typing import Union

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import HTMLResponse
from sblex.schemas import Lemma, Lexeme
from sblex.semantic_repository import SemanticRepository
from sblex.webapp.api.saldo_ws import deps
from sblex.webapp.responses import XMLResponse

router = APIRouter()


@router.get("/json/{lid}")
async def lookup_lid_json(
    lid: Union[Lexeme, Lemma],
    semantic_repo: SemanticRepository = Depends(# noqa: B008
        deps.get_saldo_semantic_repo
    ),
):
    lexeme_or_lemma = semantic_repo.get_by_lid(lid)

    return lexeme_or_lemma


@router.get(
    "/xml/{lid}",
    response_class=XMLResponse,
)
async def lookup_lid_xml(
    lid: Union[Lexeme, Lemma],
):
    xs = [
        lid,
    ]

    return lid


@router.get(
    "/html/{lid}",
    response_class=HTMLResponse,
)
async def lookup_lid_html(
    lid: Union[Lexeme, Lemma],
):
    xs = [
        lid,
    ]

    return f"{xs}"
