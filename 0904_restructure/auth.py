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


@router.post(f"/forgot-password")
async def forgot_password(request: ForgotPassword):
    user = next((u for u in fake_users_db.values() if u["email"] == request.email), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    # In a real app, send email with reset link containing token
    reset_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=15))

    # ЕМУЛЯЦІЯ ВІДПРАВКИ ЛИСТА
    print("=" * 50)
    print(f"📧 EMAIL SENT TO: {request.email}")
    print(
        f"🔗 Сlick the link to reset your password: http://localhost:8080/auth/reset-password?token={reset_token}")
    print("=" * 50)

    return {"message": "Password reset link sent to email (simulated)", "reset_token": reset_token}


@router.post(f"/reset-password")
async def reset_password(data: ResetPassword):
    try:
        if data.new_password != data.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

        username = verify_token(data.token)
        user = fake_users_db.get(username)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user["hashed_password"] = get_password_hash(data.new_password)
        return {"message": "Password reset successful"}

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid or expired token. Error: {str(error)}")
