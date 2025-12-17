from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import InboundOrder
from src.core.ports import CreateInboundOrder, InboundOrderRepository


class SqlAlchemyInboundOrderRepository(InboundOrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_or_get(self, cmd: CreateInboundOrder) -> tuple[InboundOrder, bool]:
        # 直接使用 ORM Model
        obj = InboundOrder(
            request_id=cmd.request_id,
            grn_id=cmd.grn_id,
            dock_id=cmd.dock_id,
            payload=cmd.payload,
            status="ACCEPTED",
        )
        self._session.add(obj)
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            existing = await self._session.scalar(
                select(InboundOrder).where(InboundOrder.request_id == cmd.request_id)
            )
            if existing is None:
                raise
            return existing, False
        
        await self._session.refresh(obj)
        return obj, True

    async def get(self, inbound_order_id: UUID) -> InboundOrder | None:
        return await self._session.get(InboundOrder, inbound_order_id)

    async def mark_processed(self, inbound_order_id: UUID) -> None:
        await self._session.execute(
            update(InboundOrder)
            .where(InboundOrder.inbound_order_id == inbound_order_id)
            .values(status="PROCESSED")
        )
        await self._session.commit()