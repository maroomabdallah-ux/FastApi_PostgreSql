from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import ConfigDict


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    model_config = ConfigDict(
        from_attributes=True
    )        



class UserUpdate(BaseModel):
    name: str
    email: EmailStr


class PostUpdate(BaseModel):
    title: str
    content: str    