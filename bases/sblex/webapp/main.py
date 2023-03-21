import os
from logging.config import dictConfig
from typing import Any

import asgi_correlation_id
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sblex.webapp import api, tasks


def create_app(config: dict | None = None):
    app = FastAPI()

    if not config:
        config = load_config()
    configure_logging(config or {})
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


def configure_logging(settings: dict[str, str]) -> None:  # noqa: D103
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": asgi_correlation_id.CorrelationIdFilter,
                    "uuid_length": 32,
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    # 'datefmt':  '%H:%M:%S',
                    "format": "%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s",
                },
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    # 'format': '%(message)s',
                    "format": "%(asctime)s %(levelname)s %(name)s %(process)d %(funcName)s %(lineno)d %(message)s",
                },
                "standard": {
                    "format": "%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                    # "level": 'DEBUG',
                    "stream": "ext://sys.stderr",
                },
                "json": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id"],
                    "formatter": "json",
                },
                # "email": {
                #     "class": "logging.handlers.SMTPHandler",
                #     "mailhost": "localhost",
                #     "formatter": "standard",
                #     "level": "WARNING",
                #     "fromaddr": config.LOG_MAIL_FROM,
                #     "toaddrs": config.LOG_MAIL_TOS,
                #     "subject": "Error in Karp backend!",
                # },
            },
            "loggers": {
                "sblex": {
                    "handlers": ["json"],  # ["console", "email"],
                    "level": "DEBUG",  # config.CONSOLE_LOG_LEVEL,
                    "propagate": True,
                },
                # third-party package loggers
                "sqlalchemy": {"handlers": ["json"], "level": "WARNING"},
                "uvicorn.access": {"handlers": ["json"], "level": "INFO"},
            },
        }
    )
