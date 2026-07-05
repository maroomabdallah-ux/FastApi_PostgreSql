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