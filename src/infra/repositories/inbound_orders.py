from __future__ import annotations

from datetime import timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import InboundOrder
from src.core.ports import CreateInboundOrder, InboundOrderRepository
from src.infra.database.models import InboundOrderRow


class SqlAlchemyInboundOrderRepository(InboundOrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_or_get(self, cmd: CreateInboundOrder) -> tuple[InboundOrder, bool]:
        row = InboundOrderRow(
            request_id=cmd.request_id,
            grn_id=cmd.grn_id,
            dock_id=cmd.dock_id,
            payload=cmd.payload,
            status="ACCEPTED",
        )
        self._session.add(row)
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            existing = await self._session.scalar(
                select(InboundOrderRow).where(InboundOrderRow.request_id == cmd.request_id)
            )
            if existing is None:
                raise
            return _to_domain(existing), False
        await self._session.refresh(row)
        return _to_domain(row), True

    async def get(self, inbound_order_id: UUID) -> InboundOrder | None:
        row = await self._session.get(InboundOrderRow, inbound_order_id)
        if row is None:
            return None
        return _to_domain(row)

    async def mark_processed(self, inbound_order_id: UUID) -> None:
        await self._session.execute(
            update(InboundOrderRow)
            .where(InboundOrderRow.inbound_order_id == inbound_order_id)
            .values(status="PROCESSED")
        )
        await self._session.commit()


def _to_domain(row: InboundOrderRow) -> InboundOrder:
    created_at = row.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    return InboundOrder(
        inbound_order_id=row.inbound_order_id,
        request_id=row.request_id,
        grn_id=row.grn_id,
        dock_id=row.dock_id,
        payload=row.payload,
        status=row.status,
        created_at=created_at,
    )
