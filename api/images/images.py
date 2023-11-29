from typing import Callable
from app.models.images import Image

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.controllers import ImagesController
from app.models.user import User
from app.schemas.extras.token import Token
from app.schemas.requests.images import ImagesRequest
from app.schemas.responses.images import ImagesResponse, UploadResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user

from pydantic import EmailStr


image_router = APIRouter()

@image_router.post("/upload-image", status_code=200, dependencies=[Depends(AuthenticationRequired)])
def upload_image(
    user: User = Depends(get_current_user),
    images_controller: ImagesController = Depends(Factory().get_images_controller),
    image: UploadFile = File(...),
) -> UploadResponse:
     return images_controller.save_image(user, image)

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
    