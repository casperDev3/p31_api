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

