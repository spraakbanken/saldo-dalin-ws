from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from json_streams import jsonlib

from sblex import saldo_refs
from sblex.application.queries import FullformLexQuery
from sblex.fm.morphology import Morphology
from sblex.webapp.api.saldo_ws import deps
from sblex.webapp.responses import XMLResponse

router = APIRouter()


@router.get("/json/{segment}")
async def fullform_lex_json(
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    return fullform_lex_query.query(segment=segment)


@router.get(
    "/xml/{segment}",
    response_class=XMLResponse,
)
async def fullform_xml(
    request: Request,
    segment: str,
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    templates = request.app.state.templates

    return templates.TemplateResponse(
        "saldo_fullform_lex.xml",
        context={"request": request, "j": fullform_lex_query.query(segment=segment)},
        media_type="application/xml",
    )


@router.get(
    "/html/",
    response_class=HTMLResponse,
)
@router.get(
    "/html/{segment}",
    response_class=HTMLResponse,
)
async def fullform_lex_html(
    request: Request,
    segment: Optional[str] = Query(None),  # noqa: B008
    fullform_lex_query: FullformLexQuery = Depends(  # noqa: B008
        deps.get_fullform_lex_query
    ),
):
    templates = request.app.state.templates

    if not segment:
        return templates.TemplateResponse(
            "saldo_mata_in_ordform.html",
            {
                "request": request,
                "title": "SALDO",
                "service": "fl",
                "bar": True,
            },
        )
    return templates.TemplateResponse(
        "saldo_fullform_lex.html",
        {
            "request": request,
            "title": segment,
            "service": "ff",
            "input": "",
            "bar": True,
            "segment": segment,
            "j": fullform_lex_query.query(segment=segment),
        },
    )

