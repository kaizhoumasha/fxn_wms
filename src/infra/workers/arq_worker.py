from __future__ import annotations

from urllib.parse import urlparse

from arq.connections import RedisSettings
from arq.cron import cron

from src.app.settings import Settings
from src.infra.clients.wms_client import WmsHttpClient
from src.infra.database.session import create_engine, create_sessionmaker, maybe_create_all
from src.infra.workers.tasks import deliver_outbox, process_inbound_order


async def on_startup(ctx) -> None:
    settings = Settings()
    engine = create_engine(settings.database_url)
    sessionmaker = create_sessionmaker(engine)
    if settings.auto_create_db:
        await maybe_create_all(engine)

    ctx["settings"] = settings
    ctx["db_engine"] = engine
    ctx["db_sessionmaker"] = sessionmaker
    ctx["wms_client"] = WmsHttpClient(base_url=settings.wms_base_url)


async def on_shutdown(ctx) -> None:
    await ctx["wms_client"].aclose()
    await ctx["db_engine"].dispose()


class WorkerSettings:
    functions = [process_inbound_order, deliver_outbox]
    on_startup = on_startup
    on_shutdown = on_shutdown
    cron_jobs = [cron(deliver_outbox, second=0)]

    _parsed = urlparse(Settings().redis_url)
    redis_settings = RedisSettings(
        host=_parsed.hostname or "localhost",
        port=_parsed.port or 6379,
        database=int((_parsed.path or "/0").lstrip("/") or "0"),
        password=_parsed.password,
        ssl=_parsed.scheme == "rediss",
    )
