from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.settings import Settings
from src.infra.clients.wms_client import WmsHttpClient
from src.infra.database.session import create_engine, create_sessionmaker, maybe_create_all
from src.infra.redis.client import create_redis
from src.infra.workers.arq_queue import ArqJobQueue, create_arq_pool


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()
    app.state.settings = settings
    app.state.startup_errors = {}

    engine = None
    sessionmaker = None
    try:
        engine = create_engine(settings.database_url)
        sessionmaker = create_sessionmaker(engine)
        if settings.auto_create_db:
            await maybe_create_all(engine)
    except Exception as exc:  # noqa: BLE001
        app.state.startup_errors["database"] = str(exc)
        if settings.strict_startup:
            raise

    redis = None
    try:
        redis = create_redis(settings.redis_url)
        await redis.ping()
    except Exception as exc:  # noqa: BLE001
        app.state.startup_errors["redis"] = str(exc)
        if settings.strict_startup:
            raise

    arq_pool = None
    try:
        arq_pool = await create_arq_pool(settings.redis_url)
    except Exception as exc:  # noqa: BLE001
        app.state.startup_errors["arq"] = str(exc)
        if settings.strict_startup:
            raise

    app.state.db_engine = engine
    app.state.db_sessionmaker = sessionmaker
    app.state.redis = redis
    app.state.job_queue = ArqJobQueue(arq_pool) if arq_pool is not None else None
    app.state.wms_client = WmsHttpClient(base_url=settings.wms_base_url)

    try:
        yield
    finally:
        await app.state.wms_client.aclose()
        if redis is not None:
            await redis.aclose()
        if arq_pool is not None:
            try:
                await arq_pool.close(close_connection_pool=True)
            except TypeError:
                await arq_pool.close()
        if engine is not None:
            await engine.dispose()
