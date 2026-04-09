from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
from schemas import UserRegister, UserLogin, UserResponse, ForgotPassword, ResetPassword
from security import get_password_hash, verify_password, create_access_token, verify_token
from db import fake_users_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(f"/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    return UserResponse(
        email=user.email,
        username=user.username,
        message="User registered successfully. Text: " + (user.text or "")
    )


@router.post(f"/login")
async def login(user: UserLogin):
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {
        "message": "Login successful",
        "username": user.username,
        "email": db_user["email"],
        "access_token": access_token,
        "token_type": "bearer"
    }
