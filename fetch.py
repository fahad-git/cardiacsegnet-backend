from fastapi import APIRouter, HTTPException, Depends
from io import BytesIO
from dbClient import get_data_handler


router = APIRouter()


@router.get("/image/")
async def get_image_for_user(id: int, dataset: str, handler=Depends(get_data_handler)):

    image_doc = handler.collection.find_one({"id": id, "dataset": dataset})
    
    if not image_doc:
        raise HTTPException(status_code=404, detail="No image found for the given user and dataset.")
    
    return BytesIO(image_doc["image"])
