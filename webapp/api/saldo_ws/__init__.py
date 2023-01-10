from fastapi import APIRouter

from webapp import schemas


api = APIRouter(prefix="/saldo-ws")

@api.get("/md1/{format}/{arg}")
def api_md1(format: schemas.Format, arg: schemas.Lexeme):
    ...
