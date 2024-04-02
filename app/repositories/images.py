from app.models import Image
from core.exceptions.base import NotFoundException, UnprocessableEntity
from core.repository import BaseRepository
from core.database.session import get_session_context
from fastapi import UploadFile

class ImagesRepository(BaseRepository):
    """
    Images repository provides all the database operations for the Images model.
    """

    def __init__(self):
        self.db_client = get_session_context()
        super().__init__(self.db_client, "Images")
        self.image_handler = BaseRepository(self.db_client, "Images")

    def save_image(self, userId:str, image_file: UploadFile) -> str | None:
        """
        Upload image to the server.

        :return: Image

        """
        try:
            file_location = f"data/{'org-' + userId + '-' + image_file.filename}"
            file_location_seg = f"data/{'seg-' + userId + '-' + image_file.filename}"
            file_location_xai = f"data/{'xai-' + userId + '-' + image_file.filename}"

            org_img = image_file.file.read()

            ###############################################
            #      Here will pass image to the model      #
            ###############################################

            with open(file_location, "wb+") as file_object:
                file_object.write(org_img)

            with open(file_location_seg, "wb+") as file_object:
                file_object.write(org_img)

            with open(file_location_xai, "wb+") as file_object:
                file_object.write(org_img)

            url = "/images/get-image/org-" + userId + '-' + image_file.filename
            segUrl = "/images/get-image/seg-" + userId + '-' + image_file.filename
            xaiUrl = "/images/get-image/xai-" + userId + '-' + image_file.filename

            return { "url": url, "segUrl": segUrl, "xaiUrl": xaiUrl, "filename": image_file.filename, "location": file_location } 
        except Exception as e:
            raise UnprocessableEntity("Failed to upload image.") 

    def save_image_details(self, image_details: Image) -> Image | None:
        """
        Save image details to database.

        :return: Images

        """
        response = self.image_handler.insert_document(image_details)
        if response is not None:
            return image_details
        raise UnprocessableEntity("Failed to insert record.")

    def get_image_details_list(
        self, id: str | None = None
    ) -> list[Image] | None:
        """
        Get all images by user

        :param email: Email.
        :return: List[Image].
        """
        query = {"uuid": id}
        return self.image_handler.find_all(query)

    def get_image_detail(
        self, id: str | None = None
    ) -> Image | None:
        """
        Get image detail by image id.

        :param id: str.
        :return: Image.
        """
        query = {"id": id}
        response = self.image_handler.find_document(query)
        if response is not None:
            return response
        raise NotFoundException("Cannot find information you requested")
    
    