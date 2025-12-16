from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.router import router as api_router
from src.app.lifespan import lifespan
from src.app.settings import Settings


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(title=settings.service_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app


app = create_app()

