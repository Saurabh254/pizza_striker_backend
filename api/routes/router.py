from fastapi import APIRouter

from .admin import api as admin_api
from .users import api as users_api

router = APIRouter()
router.include_router(users_api.router)
router.include_router(admin_api.router)
