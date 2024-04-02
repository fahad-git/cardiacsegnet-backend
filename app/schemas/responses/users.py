from pydantic import UUID4, BaseModel, Field


class UserResponse(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")
    uuid: str = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    name: str = Field(..., example="John Martin")