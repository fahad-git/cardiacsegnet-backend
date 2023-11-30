from pydantic import UUID4, BaseModel, Field
from fastapi import UploadFile, File

class ImagesRequest(BaseModel):
    id: str = Field(..., example="1")    
    url: str = Field(..., example="http://www.customeimage-url.com")
    reportUrl: str = Field(..., example="http://www.customereport-url.com")
    imageName: str = Field(..., example="john.doe")
    imageExtention: str = Field(..., example=".png")
    imageAnnotations: object = Field(..., example={"key1": "value1", "key2": "value2"})    
    comments: str = Field(..., example="This image is for...")

class UploadRequest(BaseModel): 
    image: UploadFile = File(...)