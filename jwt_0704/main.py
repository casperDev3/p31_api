import os

import jose
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import uvicorn

# dotenv
# import os

# config
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# PREFIX = os.getenv("PREFIX")
PREFIX = "/api/v1"

app = FastAPI(title="JWT Authentication Example", version="0.1.1")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_users_db = {}
security = HTTPBearer()


# models
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    username: str = Field(..., min_length=3, max_length=50)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    username: str
    message: str


# utils for JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# utils for password hashing
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# utils for user
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token: str = credentials.credentials
    username = verify_token(token)
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# endpoints
@app.post(f"{PREFIX}/register", status_code=status.HTTP_201_CREATED)
async def register():
    return {
        "message": "User registered successfully",
    }


@app.get("/")
async def root():
    return {
        "message": "FastAPI JWT Auth API",
        "endpoints": {
            "register": "/register (POST)",
            "login": "/login (POST)",
            "change_password": "/change-password (POST)",
            "profile": "/profile (GET) - Захищений ендпоїнт"
        }
    }


@app.get(f"{PREFIX}/health")
async def health_check():
    return {"status": "ok", "message": "API is healthy"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
