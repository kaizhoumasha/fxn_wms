from __future__ import annotations

from fastapi import APIRouter

from src.app.api.v1.health import router as health_router
from src.app.api.v1.orders import router as orders_router


router = APIRouter()
router.include_router(health_router)
router.include_router(orders_router)

