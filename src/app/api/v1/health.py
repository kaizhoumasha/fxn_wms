from __future__ import annotations

from fastapi import APIRouter
from fastapi import Request


router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health")
async def health(request: Request):
    errors = dict(getattr(request.app.state, "startup_errors", {}) or {})
    degraded = bool(errors)
    return {"status": "degraded" if degraded else "ok", "degraded": degraded, "errors": errors}
