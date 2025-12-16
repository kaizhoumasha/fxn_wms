from __future__ import annotations

from dataclasses import dataclass

from src.southbound.adapters.rcs_http import RcsHttpAdapter


@dataclass(frozen=True, slots=True)
class SouthboundGateway:
    rcs: RcsHttpAdapter

