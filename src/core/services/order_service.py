from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from src.core.models import OutboxEvent
from src.core.ports import CreateInboundOrder, InboundOrderRepository, JobQueue, OutboxRepository


class OrderService:
    def __init__(
        self,
        repo: InboundOrderRepository,
        outbox: OutboxRepository,
        jobs: JobQueue,
    ):
        self.repo = repo
        self.outbox = outbox
        self.jobs = jobs

    async def ingest_inbound_order(self, cmd: CreateInboundOrder) -> str:
        """
        接收并处理入库单
        
        Returns:
            inbound_order_id (str)
        """
        order, created = await self.repo.create_or_get(cmd)
        
        # 如果不是新建的，直接返回ID
        if not created:
            return str(order.inbound_order_id)

        # 写入 Outbox 事件
        event = OutboxEvent(
            event_id=uuid4(),
            aggregate_type="InboundOrder",
            aggregate_id=str(order.inbound_order_id),
            event_type="InboundOrderAccepted",
            payload={
                "inbound_order_id": str(order.inbound_order_id),
                "request_id": order.request_id,
                "accepted_at": datetime.now(tz=timezone.utc).isoformat(),
            },
        )
        await self.outbox.add(event)

        # 触发后台任务
        await self.jobs.enqueue(
            "process_inbound_order",
            kwargs={"inbound_order_id": str(order.inbound_order_id)},
            job_id=str(order.inbound_order_id),
        )
        
        return str(order.inbound_order_id)
