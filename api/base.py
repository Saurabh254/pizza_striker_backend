from fastapi import APIRouter

from .routes import router as api_router

router = APIRouter(prefix="/api/v1")

router.include_router(api_router.router)
