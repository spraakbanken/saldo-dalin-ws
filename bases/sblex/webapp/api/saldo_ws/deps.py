from fastapi import Depends, Request

from sblex.application.queries.lex_fullforms import FullformLexQuery
from sblex.application.services import LookupService
from sblex.fm.morphology import Morphology
from sblex.infrastructure.queries import LookupFullformLexQuery
from sblex.semantic_repository import SemanticRepository


def get_saldo_morphology(request: Request) -> Morphology:
    return request.app.state._saldo_morph


def get_saldo_semantic_repo(request: Request) -> SemanticRepository:
    return request.app.state._saldo_semantic_repo


def get_lookup_service(
    morphology: Morphology = Depends(get_saldo_morphology),  # noqa: B008
    semantic_repo: SemanticRepository = Depends(get_saldo_semantic_repo),  # noqa: B008
) -> LookupService:
    return LookupService(morphology=morphology, semantic_repo=semantic_repo)


def get_fullform_lex_query(
    lookup_service: LookupService = Depends(get_lookup_service),  # noqa: B008
) -> FullformLexQuery:
    return LookupFullformLexQuery(lookup_service=lookup_service)
