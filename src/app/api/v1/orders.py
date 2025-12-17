from __future__ import annotations

from fastapi import APIRouter, Depends

from src.app.dependencies import get_order_service
from src.app.schemas.orders import InboundOrderAccepted, InboundOrderIn
from src.core.ports import CreateInboundOrder
from src.core.services.order_service import OrderService


router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("/inbound", response_model=InboundOrderAccepted)
async def ingest_inbound_order(
    payload: InboundOrderIn,
    service: OrderService = Depends(get_order_service),
) -> InboundOrderAccepted:
    # 构造命令对象
    cmd = CreateInboundOrder(
        request_id=payload.request_id,
        grn_id=payload.grn_id,
        dock_id=payload.dock_id,
        payload=payload.model_dump(),
    )
    
    # 调用服务
    inbound_order_id = await service.ingest_inbound_order(cmd)
    
    return InboundOrderAccepted(
        request_id=payload.request_id,
        inbound_order_id=inbound_order_id,
        status="ACCEPTED",
    )