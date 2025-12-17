from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.ports import InboundOrderRepository, JobQueue, OutboxRepository
from src.core.services.order_service import OrderService
from src.infra.outbox.repository import SqlAlchemyOutboxRepository
from src.infra.repositories.inbound_orders import SqlAlchemyInboundOrderRepository


def get_settings(request: Request):
    return request.app.state.settings


def get_job_queue(request: Request) -> JobQueue:
    queue = request.app.state.job_queue
    if queue is None:
        raise HTTPException(status_code=503, detail="job queue unavailable (redis/arq not ready)")
    return queue


def get_wms_client(request: Request):
    return request.app.state.wms_client


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    sessionmaker = request.app.state.db_sessionmaker
    if sessionmaker is None:
        raise HTTPException(status_code=503, detail="database unavailable")
    async with sessionmaker() as session:
        yield session


def get_inbound_order_repo(
    session: AsyncSession = Depends(get_db_session),
) -> InboundOrderRepository:
    return SqlAlchemyInboundOrderRepository(session)


def get_outbox_repo(
    session: AsyncSession = Depends(get_db_session),
) -> OutboxRepository:
    return SqlAlchemyOutboxRepository(session)


def get_order_service(
    repo: InboundOrderRepository = Depends(get_inbound_order_repo),
    outbox: OutboxRepository = Depends(get_outbox_repo),
    jobs: JobQueue = Depends(get_job_queue),
) -> OrderService:
    return OrderService(repo=repo, outbox=outbox, jobs=jobs)