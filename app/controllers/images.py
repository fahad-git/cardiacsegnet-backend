from pydantic import EmailStr
from fastapi import UploadFile
from fastapi import HTTPException

from app.models import Image, AnnotationUpdateModel
from app.models.user import User
from app.schemas.requests.images import ImagesRequest
from core.controller import BaseController
from app.repositories import ImagesRepository
import copy
from app.repositories.images import ImagesRepository
import os
import uuid
from app.models.user import User


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
            "segUrl": image_details.segUrl,
            "xaiUrl": image_details.xaiUrl,
            "imageName": image_details.imageName,
            "reportUrl": image_details.reportUrl,
            "imageExtention": image_details.imageExtention,
            "imageAnnotations": image_details.imageAnnotations,
            "comments": image_details.comments
        }
        return self.images_repository.save_image_details(image_details_with_user)

    def save_image(self, user: User, image_file: UploadFile) -> str:
        return self.images_repository.save_image(userId=user["uuid"], image_file=image_file)
