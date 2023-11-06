from fastapi import APIRouter

from .users import user_router
from .images import images_router

router = APIRouter()
router.include_router(user_router, prefix="/api")
router.include_router(images_router, prefix="/api")

__all__ = ["router"]