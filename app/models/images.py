from pydantic import BaseModel, Field

class Image(BaseModel):
    id: str
    url: str 
    imageName: str   
    imageExtention: str 
    # imageAnnotations: object
    comments: str
