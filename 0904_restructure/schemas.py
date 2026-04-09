from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    username: str = Field(..., min_length=3, max_length=50)
    text: Optional[str] = None


class UpdateProfile(BaseModel):
    email: Optional[EmailStr] = None
    text: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    username: str
    message: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)
