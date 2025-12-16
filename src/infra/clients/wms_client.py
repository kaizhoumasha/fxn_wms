from __future__ import annotations

import httpx


class WmsHttpClient:
    def __init__(self, *, base_url: str):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=10.0)

    async def post_inventory_putaway(self, payload: dict) -> None:
        await self._client.post("/api/wms/inventory/putaway", json=payload)

    async def aclose(self) -> None:
        await self._client.aclose()

