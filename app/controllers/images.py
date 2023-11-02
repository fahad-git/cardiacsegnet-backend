from pydantic import EmailStr
from app.models import Image
from app.models.user import User
from app.schemas.requests.images import ImagesRequest
from core.controller import BaseController
from app.repositories import ImagesRepository
import copy


class ImagesController(BaseController):
    def __init__(self, images_repository: ImagesRepository):
        super().__init__(model=Image, repository=images_repository)
        self.images_repository = images_repository

    def get_image_detail(self, id: str) -> Image:
        return self.images_repository.get_image_detail(id)

    def get_images_by_user(self, id: str) -> list[Image]:
        return self.images_repository.get_image_details_list(id)
    
    def save_image_details(self, image_details: Image, user: User) -> Image:
        image_details_with_user: Image = {
            "uuid": user["uuid"],
            "id": image_details.id,
            "url": image_details.url,
            "imageName": image_details.imageName,
            "imageExtention": image_details.imageExtention,
            "comments": image_details.comments
        }
        return self.images_repository.save_image_details(image_details_with_user)
