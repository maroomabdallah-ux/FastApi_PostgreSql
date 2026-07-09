from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import ConfigDict
from decimal import Decimal


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


############################### USER

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )


class UserUpdate(BaseModel):
    name: str
    email: EmailStr

################################### POST
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




class PostUpdate(BaseModel):
    title: str
    content: str    
#################################### PRODUCT

class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    stock_quantity: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stock_quantity: int

    model_config = ConfigDict(
        from_attributes=True
    )


class UserProductCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class UserProductResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(
        from_attributes=True
    )




class UserProductResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(
        from_attributes=True
    )


class MyProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    quantity: int

    model_config = ConfigDict(
        from_attributes=True
    )
