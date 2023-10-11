from pydantic import BaseModel, Field


class Data(BaseModel):
    image: bytes 
    pdf: bytes   
    comment: str
    uploaded_by: str 
    dataset: int


class User(BaseModel):
    username: str = Field(..., max_length=100)
    password: str  
    # Will store hashed passwords later
