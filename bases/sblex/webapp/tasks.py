from typing import Callable

from fastapi import FastAPI
from sblex.fm.morphology import Morphology


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        load_saldo_morphology(app)

    return start_app


def load_saldo_morphology(app: FastAPI) -> None:
    saldo_morphology = Morphology(app.state.config["SALDO_MORPHOLOGY_PATH"])
    saldo_morphology.build()
    app.state._saldo_morph = saldo_morphology
