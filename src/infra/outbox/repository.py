from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import OutboxEvent
from src.core.ports import OutboxRepository
from src.infra.database.models import OutboxRow


class SqlAlchemyOutboxRepository(OutboxRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, event: OutboxEvent) -> None:
        row = OutboxRow(
            event_id=event.event_id,
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            event_type=event.event_type,
            payload=event.payload,
            status="PENDING",
            attempts=0,
        )
        self._session.add(row)
        await self._session.commit()

    async def claim_batch(self, *, limit: int) -> list[OutboxEvent]:
        stmt = (
            select(OutboxRow)
            .where(OutboxRow.status == "PENDING")
            .order_by(OutboxRow.id)
            .with_for_update(skip_locked=True)
            .limit(limit)
        )
        rows = (await self._session.scalars(stmt)).all()
        for row in rows:
            row.status = "INFLIGHT"
            row.attempts += 1
        await self._session.commit()
        return [OutboxEvent(r.event_id, r.aggregate_type, r.aggregate_id, r.event_type, r.payload) for r in rows]

    async def mark_delivered(self, event_id: UUID) -> None:
        await self._session.execute(
            update(OutboxRow).where(OutboxRow.event_id == event_id).values(status="DELIVERED")
        )
        await self._session.commit()

    async def mark_failed(self, event_id: UUID, *, error: str) -> None:
        await self._session.execute(
            update(OutboxRow).where(OutboxRow.event_id == event_id).values(status="FAILED", last_error=error)
        )
        await self._session.commit()
