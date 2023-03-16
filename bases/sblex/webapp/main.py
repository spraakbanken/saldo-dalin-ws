import os
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sblex.webapp import api, tasks


def create_app(config: dict | None = None):
    app = FastAPI()

    if not config:
        config = load_config()

    app.state.config = config
    app.state.templates = Jinja2Templates(
        directory=config.get("APP_TEMPLATES", "templates")
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))

    app.include_router(api.router)

    return app


def load_config() -> dict[str, Any]:
    load_dotenv(".env", verbose=True)
    return {
        "SALDO_MORPHOLOGY_PATH": os.environ.get("SALDO_MORPHOLOGY_PATH","assets/testing/saldo.lex"),
        "SALDO_SEMANTIC_PATH": os.environ.get("SALDO_SEMANTIC_PATH", "assets/testing/saldo.txt"),
    }
