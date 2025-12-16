from __future__ import annotations

import httpx


class RcsHttpAdapter:
    def __init__(self, *, base_url: str):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=10.0)

    async def transport(self, payload: dict) -> dict:
        resp = await self._client.post("/task", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def aclose(self) -> None:
        await self._client.aclose()

