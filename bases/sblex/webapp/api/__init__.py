from fastapi import APIRouter

from sblex.webapp.api import saldo_ws


router = APIRouter()

router.include_router(saldo_ws.router, prefix="/saldo-ws", tags=["saldo"])
