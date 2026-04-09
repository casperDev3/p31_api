from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UpdateProfile(BaseModel):
    email: Optional[EmailStr] = None
    text: Optional[str] = None
