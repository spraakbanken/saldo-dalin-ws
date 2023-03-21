from fastapi import APIRouter
from sblex.webapp.api.saldo_ws import fullform_api, fullform_lex_api, lids, md1_api

router = APIRouter()

router.include_router(md1_api.router, prefix="/md1", tags=["md1"])
router.include_router(fullform_api.router, prefix="/ff", tags=["fullform"])
router.include_router(fullform_lex_api.router, prefix="/fl", tags=["fullform_lex"])
router.include_router(lids.router, prefix="/lid", tags=["lid", "lemma-id", "saldo-id"])
