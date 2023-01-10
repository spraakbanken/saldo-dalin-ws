from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp import api


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api.router)

    return app


