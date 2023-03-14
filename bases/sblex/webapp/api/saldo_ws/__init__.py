from fastapi import APIRouter
from sblex.webapp.api.saldo_ws import fullform_api, md1_api

router = APIRouter()

router.include_router(md1_api.router, prefix="/md1", tags=["md1"])
router.include_router(fullform_api.router, prefix="/ff", tags=["fullform"])
