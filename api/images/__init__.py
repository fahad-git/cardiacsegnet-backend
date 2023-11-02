from fastapi import APIRouter

from .images import image_router

images_router = APIRouter()
images_router.include_router(image_router, prefix="/images", tags=["Images"])

__all__ = ["images_router"]