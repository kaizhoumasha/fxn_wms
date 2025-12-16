from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.core.models import InboundOrder, OutboxEvent
from src.core.ports import CreateInboundOrder, InboundOrderRepository, JobQueue, OutboxRepository


@dataclass(frozen=True, slots=True)
class IngestResult:
    """
    表示订单接收处理结果的数据类
    
    Attributes:
        inbound_order_id: 入站订单的唯一标识符
    """
    inbound_order_id: UUID


@dataclass(frozen=True, slots=True)
class IngestInboundOrder:
    """
    处理入站订单的用例类
    
    负责接收、创建入站订单，并触发后续处理流程，包括发送事件和安排任务队列。
    
    Attributes:
        repo: 入站订单仓库，用于持久化订单数据
        outbox: 事件仓库，用于发布领域事件
        jobs: 任务队列，用于安排异步任务
    """
    repo: InboundOrderRepository
    outbox: OutboxRepository
    jobs: JobQueue

    async def handle(self, inbound_payload) -> IngestResult:
        """
        处理入站订单
        
        如果订单已存在则直接返回，否则创建新订单并触发后续处理流程。
        
        Args:
            inbound_payload: 入站订单的有效载荷数据
            
        Returns:
            IngestResult: 包含处理后的入站订单ID的结果对象
        """
        cmd = CreateInboundOrder(
            request_id=inbound_payload.request_id,
            grn_id=inbound_payload.grn_id,
            dock_id=inbound_payload.dock_id,
            payload=inbound_payload.model_dump(),
        )

        # 尝试创建订单，如果已存在则返回现有订单
        order, created = await self.repo.create_or_get(cmd)
        if not created:
            return IngestResult(inbound_order_id=order.inbound_order_id)

        # 创建订单接收事件
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

        # 安排处理入站订单的异步任务
        await self.jobs.enqueue(
            "process_inbound_order",
            kwargs={"inbound_order_id": str(order.inbound_order_id)},
            job_id=str(order.inbound_order_id),
        )
        return IngestResult(inbound_order_id=order.inbound_order_id)