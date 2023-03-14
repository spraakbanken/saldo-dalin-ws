from fastapi import Request
from sblex.fm.morphology import Morphology


def get_saldo_morphology(request: Request) -> Morphology:
    return request.app.state._saldo_morph
