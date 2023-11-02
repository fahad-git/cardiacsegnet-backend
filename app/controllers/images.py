from pydantic import EmailStr
from app.models import Image
from core.controller import BaseController
from app.repositories import ImagesRepository


class ImagesController(BaseController):
    def __init__(self, images_repository: ImagesRepository):
        super().__init__(model=Image, repository=images_repository)
        self.images_repository = images_repository

    def get_image_detail(self, id: str) -> Image:
        return self.images_repository.get_image_detail(id)

    def get_images_by_user(self, email: EmailStr) -> list[Image]:
        return self.images_repository.get_image_details_list(email)
