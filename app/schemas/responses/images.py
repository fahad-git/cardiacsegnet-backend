from pydantic import UUID4, BaseModel, Field


class ImagesResponse(BaseModel):
    id: str = Field(..., example="1")    
    url: str = Field(..., example="http://www.customeimage-url.com")
    imageName: str = Field(..., example="john.doe")
    imageExtention: str = Field(..., example=".png")
    # imageAnnotations: object = Field(..., example="{{1, 2, 3, 4, 5, 6, 7, 8}}")    
    comments: str = Field(..., example="This image is for...")