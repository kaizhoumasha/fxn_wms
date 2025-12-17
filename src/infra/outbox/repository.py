from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import OutboxEvent
from src.core.ports import OutboxRepository


class SqlAlchemyOutboxRepository(OutboxRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, event: OutboxEvent) -> None:
        # event 已经是 ORM 对象了，直接 add
        self._session.add(event)
        await self._session.commit()

    async def claim_batch(self, *, limit: int) -> list[OutboxEvent]:
        stmt = (
            select(OutboxEvent)
            .where(OutboxEvent.status == "PENDING")
            .order_by(OutboxEvent.id)
            .with_for_update(skip_locked=True)
            .limit(limit)
        )
        events = (await self._session.scalars(stmt)).all()
        for event in events:
            event.status = "INFLIGHT"
            event.attempts += 1
        await self._session.commit()
        # 直接返回 ORM 对象列表
        return list(events)

    async def mark_delivered(self, event_id: UUID) -> None:
        await self._session.execute(
            update(OutboxEvent).where(OutboxEvent.event_id == event_id).values(status="DELIVERED")
        )
        await self._session.commit()

    async def mark_failed(self, event_id: UUID, *, error: str) -> None:
        await self._session.execute(
            update(OutboxEvent).where(OutboxEvent.event_id == event_id).values(status="FAILED", last_error=error)
        )
        await self._session.commit()