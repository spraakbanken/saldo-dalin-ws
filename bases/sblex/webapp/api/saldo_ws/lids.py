from typing import Union

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Request,
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
    name="saldo-ws:lid-html"
)
async def lookup_lid_html(
    request: Request,
    lid: Lexeme,
    semantic_repo: SemanticRepository = Depends(# noqa: B008
        deps.get_saldo_semantic_repo
    ),
):
    templates = request.app.state.templates
    lexeme_or_lemma = semantic_repo.get_by_lid(lid)

    print(f"{lexeme_or_lemma=}")
    if lexeme_or_lemma == []:
        return templates.TemplateResponse("saldo_lid_saknas.html", context={"request": request, "lid": lid, "bar": False})

    return f"{lexeme_or_lemma}"


def htmlize_lemma(lid, s):
    j = cjson.decode(utf8.d(s))
    if not (j == []):
        return table.function("html", utf8.e(j["p"]), utf8.e(j["gf"]))[0]
    else:
        content = "<center><p><b>" + lid + " finns ej.</b></p></center>"
        html = saldo_util.html_document(lid, content, bar=False)
        return html


def htmlize_lexeme(lexeme, s):
    j = cjson.decode(utf8.d(s))
    if j == []:
        result = "<center>%s finns ej.</center>" % lexeme
    else:
        fm = saldo_util.lexeme_ref(utf8.e(j["fm"]))
        fp = saldo_util.lexeme_ref(utf8.e(j["fp"]))
        pf_len = len(j["pf"])
        mf_len = len(j["mf"])
        if pf_len == 0:
            pf_len = ""
        else:
            pf_len = "<br />" + str(pf_len)
        if mf_len == 0:
            mf_len = ""
        else:
            mf_len = "<br />" + str(mf_len)
        fmmf_len = 0
        mf = sort_children(j["mf"], "p")
        if lexeme == "PRIM..1":
            pf = "*"
            lem = ""
        else:
            pf = sort_children(j["pf"], "m")
            lem = ", ".join([saldo_util.lemma_href(utf8.e(l)) for l in j["l"]])
        result = """
     <h1>%s</h1>
     <center><table border="1">
     <tr><td style="text-align:center;">⇧[%d]</td><td>%s</td>
    <td style="text-align:center;">↑</td><td>%s</td></tr>
    </table>
      <p>%s<br/>%s <br /> %s</p>
    <table border="1">
    <tr><td style="vertical-align:top;text-align:center;">⇩%s</td><td style="vertical-align:top;">%s</td>
    <td style="vertical-align:top;text-align:center;">↓%s</td><td style="vertical-align:top;">%s</td></tr>
   </table></center>
""" % (
            saldo_util.prlex(utf8.e(j["lex"])),
            depth(j["lex"], j["path"]),
            fm,
            fp,
            lem,
            saldo_util.graph(j["lex"]),
            saldo_util.korpus_ref(j["l"], "[korpus]"),
            mf_len,
            mf,
            pf_len,
            pf,
        )
    return saldo_util.html_document(lexeme, result)
