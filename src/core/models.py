from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class InboundOrder:
    inbound_order_id: UUID
    request_id: str
    grn_id: str
    dock_id: str
    payload: dict
    status: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class OutboxEvent:
    event_id: UUID
    aggregate_type: str
    aggregate_id: str
    event_type: str
    payload: dict

