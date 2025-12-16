from __future__ import annotations

from uuid import UUID

from src.infra.clients.wms_client import WmsHttpClient
from src.infra.outbox.repository import SqlAlchemyOutboxRepository
from src.infra.repositories.inbound_orders import SqlAlchemyInboundOrderRepository


async def process_inbound_order(ctx, inbound_order_id: str) -> None:
    sessionmaker = ctx["db_sessionmaker"]

    async with sessionmaker() as session:
        repo = SqlAlchemyInboundOrderRepository(session)
        order = await repo.get(UUID(inbound_order_id))
        if order is None:
            return
        await repo.mark_processed(UUID(inbound_order_id))


async def deliver_outbox(ctx) -> None:
    sessionmaker = ctx["db_sessionmaker"]
    wms: WmsHttpClient = ctx["wms_client"]

    async with sessionmaker() as session:
        outbox = SqlAlchemyOutboxRepository(session)
        events = await outbox.claim_batch(limit=50)
        for event in events:
            try:
                if event.event_type == "InboundOrderAccepted":
                    await wms.post_inventory_putaway(event.payload)
                await outbox.mark_delivered(event.event_id)
            except Exception as exc:  # noqa: BLE001
                await outbox.mark_failed(event.event_id, error=str(exc))
