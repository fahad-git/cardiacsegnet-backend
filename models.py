from pydantic import BaseModel, Field


class Data(BaseModel):
    id: int
    image: bytes 
    pdf: bytes   
    comment: str
    uploaded_by: str 
    dataset: int


class User(BaseModel):
    id:int = None
    username: str = Field(..., max_length=100)
    password: str  
    # Will store hashed passwords later

class NewUser(BaseModel):
    username: str
    password: str
