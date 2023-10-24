from pydantic import BaseModel, Field

class Data(BaseModel):
    id: int
    image: bytes 
    pdf: bytes   
    comment: str
    uploaded_by: str 
    dataset: int
