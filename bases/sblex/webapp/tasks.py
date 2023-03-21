from typing import Callable

from fastapi import FastAPI
from sblex.fm import Morphology
from sblex.semantic_repository import SemanticRepository
from sblex.mem_semantic_repository import MemSemanticRepository


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        load_saldo_morphology(app)
        load_saldo_semantic_repo(app)

    return start_app


def load_saldo_morphology(app: FastAPI) -> None:
    saldo_morphology = Morphology.from_path(app.state.config["SALDO_MORPHOLOGY_PATH"])
    app.state._saldo_morph = saldo_morphology


def load_saldo_semantic_repo(app: FastAPI) -> None:
    saldo_semantic_repo = MemSemanticRepository.from_tsv_path(
        app.state.config["SALDO_SEMANTIC_PATH"]
    )
    app.state._saldo_semantic_repo = saldo_semantic_repo
