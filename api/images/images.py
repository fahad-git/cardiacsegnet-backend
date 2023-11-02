from typing import Callable

from fastapi import APIRouter, Depends

from app.controllers import ImagesController
from app.schemas.extras.token import Token
from app.schemas.requests.images import ImagesRequest
from app.schemas.responses.images import ImagesResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from pydantic import EmailStr

image_router = APIRouter()

# @user_router.get("/upload-image", dependencies=[Depends(AuthenticationRequired)])
# async def get_users(
#     user_controller: UserController = Depends(Factory().get_user_controller),
#     assert_access: Callable = Depends(Permissions(UserPermission.READ)),
# ) -> list[UserResponse]:
#     users = user_controller.get_all()
#     # assert_access(resource=users)
#     return users

@image_router.get("/get-image-details", dependencies=[Depends(AuthenticationRequired)])
async def get_image_details(
    imageId: str,
    images_controller: ImagesController = Depends(Factory().get_images_controller),
) -> ImagesResponse:
    return images_controller.get_image_detail(id = imageId)


@image_router.get("/get-images-by-user", dependencies=[Depends(AuthenticationRequired)])
async def get_images_by_user(
    userEmail: EmailStr,
    images_controller: ImagesController = Depends(Factory().get_images_controller),
) -> list[ImagesResponse]:
    return images_controller.get_images_by_user(userEmail)