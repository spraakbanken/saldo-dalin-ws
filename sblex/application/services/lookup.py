from typing import Any

from json_streams import jsonlib

from sblex.fm import Morphology
from sblex.semantic_repository.core import SemanticRepository


class LookupService:
    def __init__(
        self, *, morphology: Morphology, semantic_repo: SemanticRepository
    ) -> None:
        self._morphology = morphology
        self._semantic_repo = semantic_repo

    def lookup_ff(self, segment: str) -> list[dict[str, Any]]:
        return jsonlib.loads(self._morphology.lookup(segment))["a"]

    def lookup_lid(self, lid: str) -> dict[str, Any]:
        return self._semantic_repo.get_by_lid(lid)
