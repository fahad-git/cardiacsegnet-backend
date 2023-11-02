from pydantic import UUID4, BaseModel, Field


class ImagesRequest(BaseModel):
    id: str = Field(..., example="1")    
    url: str = Field(..., example="http://www.customeimage-url.com")
    imageName: str = Field(..., example="john.doe")
    # imageAnnotations: object = Field(..., example="{{1, 2, 3, 4, 5, 6, 7, 8}}")
    imageExtention: str = Field(..., example=".png")
    comments: str = Field(..., example="This image is for...")