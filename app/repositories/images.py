from app.models import Image
from core.repository import BaseRepository
import asyncio
from core.database.session import get_session_context
from pydantic import EmailStr

class ImagesRepository(BaseRepository):
    """
    Images repository provides all the database operations for the Images model.
    """

    def __init__(self):
        self.db_client = get_session_context()
        super().__init__(self.db_client, "Images")
        self.image_handler = BaseRepository(self.db_client, "Images")

    def upload_image(self, image: Image) -> Image | None:
        """
        Upload image to the server.

        :return: Image

        """
        return self.image_handler.insert_document(image)

    def save_image_details(self) -> Image | None:
        """
        Save image details to database.

        :return: Images

        """
        return self.image_handler.insert_document(Image)

    def get_image_details_list(
        self, email: EmailStr | None = None
    ) -> list[Image] | None:
        """
        Get all images by user

        :param email: Email.
        :return: List[Image].
        """
        return self.image_handler.find_all()

    def get_image_detail(
        self, id: str | None = None
    ) -> Image | None:
        """
        Get image detail by image id.

        :param id: str.
        :return: Image.
        """
        query = {"id": id}
        return self.image_handler.find_document(query)