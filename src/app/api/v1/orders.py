from __future__ import annotations

from fastapi import APIRouter, Depends

from src.app.dependencies import get_ingest_inbound_order_use_case
from src.app.schemas.orders import InboundOrderAccepted, InboundOrderIn
from src.core.use_cases.ingest_inbound_order import IngestInboundOrder


router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("/inbound", response_model=InboundOrderAccepted)
async def ingest_inbound_order(
    payload: InboundOrderIn,
    use_case: IngestInboundOrder = Depends(get_ingest_inbound_order_use_case),
) -> InboundOrderAccepted:
    result = await use_case.handle(payload)
    return InboundOrderAccepted(
        request_id=payload.request_id,
        inbound_order_id=str(result.inbound_order_id),
        status="ACCEPTED",
    )

