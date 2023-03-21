from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from json_streams import jsonlib

from sblex.fm.morphology import Morphology
from sblex.webapp.api.saldo_ws import deps
from sblex.webapp.responses import XMLResponse

router = APIRouter()


@router.get("/json/{fragment}")
async def fullform_json(
    fragment: str,
    morphology: Morphology = Depends(deps.get_saldo_morphology),  # noqa: B008
):
    return Response(
        content=morphology.lookup(fragment),
        media_type="application/json",
    )


@router.get(
    "/xml/{fragment}",
    response_class=XMLResponse,
)
async def fullform_xml(
    request: Request,
    fragment: str,
    morphology: Morphology = Depends(deps.get_saldo_morphology),  # noqa: B008
):
    templates = request.app.state.templates

    return templates.TemplateResponse(
        "saldo_fullform.xml",
        context={
            "request": request,
            "j": jsonlib.loads(morphology.lookup(fragment)),
        },
        media_type="application/xml",
    )


@router.get(
    "/html/{fragment}",
    response_class=HTMLResponse,
)
async def fullform_html(
    request: Request,
    fragment: str,
    morphology: Morphology = Depends(deps.get_saldo_morphology),  # noqa: B008
):
    templates = request.app.state.templates

    return templates.TemplateResponse(
        "saldo_fullform.html",
        {
            "request": request,
            "title": fragment,
            "service": "ff",
            "input": "",
            "bar": True,
            "segment": fragment,
            "j": jsonlib.loads(morphology.lookup(fragment))
            # "content": htmlize(fragment, morphology.lookup(f"0 {fragment}".encode("utf-8")))
        },
    )
