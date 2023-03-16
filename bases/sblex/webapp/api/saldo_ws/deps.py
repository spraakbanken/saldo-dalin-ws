from fastapi import Request
from sblex.fm.morphology import Morphology
from sblex.semantic_repository import SemanticRepository


def get_saldo_morphology(request: Request) -> Morphology:
    return request.app.state._saldo_morph


def get_saldo_semantic_repo(request: Request) -> SemanticRepository:
    return request.app.state._saldo_semantic_repo
