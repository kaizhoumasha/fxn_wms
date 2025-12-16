from __future__ import annotations

from pydantic import BaseModel, Field


class InboundOrderLineIn(BaseModel):
    line_id: str
    material_id: str
    vendor_id: str
    qty: int = Field(ge=1)
    uom: str = "EA"
    dc: str
    lc: str | None = None
    tray_size_inch: int = Field(default=7, ge=1)
    tray_thickness_mm: float | None = Field(default=None, ge=0)


class InboundOrderIn(BaseModel):
    request_id: str
    grn_id: str
    dock_id: str
    lines: list[InboundOrderLineIn]
    allow_mixed_pallet: bool = True


class InboundOrderAccepted(BaseModel):
    request_id: str
    inbound_order_id: str
    status: str

