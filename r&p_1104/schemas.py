from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Optional

# review schemas
class ReviewBase(BaseModel):
    rating: int
    text: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

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

# user schemas
class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    text: Optional[str] = None
    role: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    