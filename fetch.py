# from fastapi import APIRouter, HTTPException
# from io import BytesIO
# from core.database.dbClient import data_handler


# router = APIRouter()


# @router.get("/image/")
# async def get_image_for_user(id: int, dataset: int):

#     image_doc = data_handler.collection.find_one({"id": id, "dataset": dataset})
    
#     if not image_doc:
#         raise HTTPException(status_code=404, detail="No image found for the given user and dataset.")
    
#     return BytesIO(image_doc["image"])
