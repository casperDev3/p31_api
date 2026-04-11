from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Optional


# review schemas
class ReviewBase(BaseModel):
    rating: int
    text: Optional[str] = None


class ReviewCreate(ReviewBase):
    product_id: int


class ReviewResponse(ReviewBase):
    id: int
    product_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)





# product schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    user_id: int
    reviews: List[ReviewResponse] = []

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    message: str
    username: str
    email: str
    role: str
    access_token: str
    token_type: str = "bearer"

# user schemas
class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str
    text: Optional[str] = None


class UserResponse(UserBase):
    id: int
    text: Optional[str] = None
    role: str
    message: Optional[str] = None
    reviews: List[ReviewResponse] = []
    products: List[ProductResponse] = []

    model_config = ConfigDict(from_attributes=True)
