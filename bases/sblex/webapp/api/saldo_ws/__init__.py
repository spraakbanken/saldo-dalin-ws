from fastapi import APIRouter

from sblex.webapp.api.saldo_ws import md1_api


router = APIRouter()

router.include_router(md1_api.router, prefix="/md1", tags=["md1"])
