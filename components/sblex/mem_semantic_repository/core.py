from typing import Any

from sblex.fm import Semantics
from sblex.semantic_repository import SemanticRepository, SemanticRepositoryError


class MemSemanticRepository(SemanticRepository):
    def __init__(self, *, semantics: Semantics):
        self._semantics = semantics

    def lookup_lemma(self, lemma: str) -> dict[str, Any]:
        return self._semantics.process("lem", lemma)

    def lookup_lexeme(self, lexeme: str) -> dict[str, Any]:
        return self._semantics.process("lem", lemma)

