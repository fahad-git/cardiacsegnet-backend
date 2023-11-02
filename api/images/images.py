from typing import Callable

from fastapi import APIRouter, Depends

from app.controllers import ImagesController
from app.models.user import User
from app.schemas.extras.token import Token
from app.schemas.requests.images import ImagesRequest
from app.schemas.responses.images import ImagesResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from pydantic import EmailStr

from core.fastapi.dependencies.current_user import get_current_user

image_router = APIRouter()

@image_router.post("/save-image-details", status_code=200, dependencies=[Depends(AuthenticationRequired)])
def save_image_details(
    image_details: ImagesRequest,
    user: User = Depends(get_current_user),
    images_controller: ImagesController = Depends(Factory().get_images_controller),
) -> ImagesResponse:
    return images_controller.save_image_details(image_details, user)

@image_router.get("/get-image-details", dependencies=[Depends(AuthenticationRequired)])
async def get_image_details(
    imageId: str,
    images_controller: ImagesController = Depends(Factory().get_images_controller),
) -> ImagesResponse:
    return images_controller.get_image_detail(id = imageId)


@image_router.get("/get-images-by-user", dependencies=[Depends(AuthenticationRequired)])
async def get_images_by_user(
    user: User = Depends(get_current_user),
    images_controller: ImagesController = Depends(Factory().get_images_controller),
) -> list[ImagesResponse]:
    return images_controller.get_images_by_user(user["uuid"])