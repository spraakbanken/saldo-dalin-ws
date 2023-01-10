from fastapi import APIRouter

from webapp.api import saldo_ws


router = APIRouter()

router.include_router(saldo_ws.router, prefix="/saldo-ws", tags=["saldo"])
