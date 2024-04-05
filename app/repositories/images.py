from app.models import Image
from core.exceptions.base import NotFoundException, UnprocessableEntity
from core.repository import BaseRepository
from core.database.session import get_session_context
from fastapi import UploadFile
import core.utility.image_module as im
import os

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
            base_file_name = str(image_file.filename).split(".")[0]
            base_dir_path = userId + "-" + base_file_name

            os.makedirs(f"data/" + base_dir_path, exist_ok=True)

            org_file_location = f"data/{base_dir_path}/org-{userId}-{image_file.filename}"
            # pass file to the model.
            # model will create segmented image and save it here.
            seg_file_location = f"data/{base_dir_path}/seg-{userId}-{image_file.filename}"
            # pass file to XAI module
            # model will create xai image and save it here.
            xai_file_location = f"data/{base_dir_path}/xai-{userId}-{image_file.filename}"

            ###############################################
            #      Here will pass image to the model      #
            ###############################################
            org_img = image_file.file.read()
            seg_img = org_img # this will come from model
            xai_img = org_img # this will come from model

            with open(org_file_location, "wb+") as file_object:
                file_object.write(org_img)

            with open(seg_file_location, "wb+") as file_object:
                file_object.write(seg_img) # later, seg_img will come from model

            with open(xai_file_location, "wb+") as file_object:
                file_object.write(xai_img) # later, xai_img will come from model
            
            orgUrl = f"/images/get-image/{base_dir_path}/org-{userId}-{image_file.filename}"
            segUrl = f"/images/get-image/{base_dir_path}/seg-{userId}-{image_file.filename}"
            xaiUrl = f"/images/get-image/{base_dir_path}/xai-{userId}-{image_file.filename}"
            
            orgDim1Url = f"/images/get-image/{base_dir_path}/org-dim-1-{userId}-{base_file_name}.png"
            orgDim2Url = f"/images/get-image/{base_dir_path}/org-dim-2-{userId}-{base_file_name}.png"
            orgDim3Url = f"/images/get-image/{base_dir_path}/org-dim-3-{userId}-{base_file_name}.png"

            segDim1Url = f"/images/get-image/{base_dir_path}/seg-dim1-{userId}-{base_file_name}.png"
            segDim2Url = f"/images/get-image/{base_dir_path}/seg-dim2-{userId}-{base_file_name}.png"
            segDim3Url = f"/images/get-image/{base_dir_path}/seg-dim3-{userId}-{base_file_name}.png"

            xaiDim1Url = f"/images/get-image/{base_dir_path}/xai-dim1-{userId}-{base_file_name}.png"
            xaiDim2Url = f"/images/get-image/{base_dir_path}/xai-dim2-{userId}-{base_file_name}.png"
            xaiDim3Url = f"/images/get-image/{base_dir_path}/xai-dim3-{userId}-{base_file_name}.png"
            
            # for file names
            org_file_names = [os.path.basename(orgDim1Url), os.path.basename(orgDim2Url), os.path.basename(orgDim3Url)]
            seg_file_names = [os.path.basename(segDim1Url), os.path.basename(segDim2Url), os.path.basename(segDim3Url)]
            xai_file_names = [os.path.basename(xaiDim1Url), os.path.basename(xaiDim2Url), os.path.basename(xaiDim3Url)]

            im.save_slice_as_image(org_file_location, f"data/" + base_dir_path, org_file_names)

            im.save_slice_as_image(seg_file_location, f"data/" + base_dir_path, seg_file_names)

            im.save_slice_as_image(xai_file_location, f"data/" + base_dir_path, xai_file_names)
   

            return {"orgUrl": orgUrl, 
                    "segUrl": segUrl, 
                    "xaiUrl": xaiUrl, 
                    "orgDim1Url": orgDim1Url, "orgDim2Url": orgDim2Url, "orgDim3Url": orgDim3Url, 
                    "segDim1Url": segDim1Url, "segDim2Url": segDim2Url, "segDim3Url": segDim3Url, 
                    "xaiDim1Url": xaiDim1Url, "xaiDim2Url": xaiDim2Url,  "xaiDim3Url": xaiDim3Url,  
                    "filename": image_file.filename, 
                    "location": org_file_location } 
        
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
    
    