from fastapi import APIRouter

from .users import user_router

router = APIRouter()
router.include_router(user_router, prefix="/api")

__all__ = ["router"]