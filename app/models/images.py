from pydantic import BaseModel, Field

class Image(BaseModel):
    uuid: str
    id: str
    url: str 
    imageName: str   
    imageExtention: str 
    # imageAnnotations: object
    comments: str
