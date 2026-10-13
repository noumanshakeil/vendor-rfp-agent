from fastapi import APIRouter
from backend.api import health, requirements, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(requirements.router, prefix="/api/requirements", tags=["requirements"])
api_router.include_router(ui.router, tags=["ui"])
