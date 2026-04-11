from fastapi import FastAPI, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Product, User, Review
from schemas import ProductCreate, ProductResponse, UserResponse, UserCreate, UserLogin, UserLoginResponse, \
    ReviewCreate, ReviewResponse
from security import create_access_token, verify_password, get_password_hash, get_current_user
from typing import List

import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="R&P 1104", version="0.4.0")
PREFIX = "/api/v1"


# ======= AUTH & USERS ENDPOINTS =======
@app.post(f"{PREFIX}/register", response_model=UserResponse, status_code=201, tags=["Auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create new user (for simplicity, using Product model as User)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)  # In real app, hash the password!
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        message="User registered successfully. Text: " + (user.text or ""),
        role=new_user.role,
    )


@app.post(f"{PREFIX}/login/", tags=["Auth"])
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return UserLoginResponse(
        message="Login successful",
        username=user.username,
        email=user.email,
        access_token=access_token,
        token_type="bearer",
        role=user.role,
    )

@app.get(f"{PREFIX}/users", response_model=List[UserResponse], tags=["Auth"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# ======= PRODUCTS ENDPOINTS =======
@app.post(f"{PREFIX}/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    new_product = Product(**product.model_dump(), user_id=current_user.id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get(f"{PREFIX}/products", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# ===== REVIEW ENDPOINTS =======
@app.post(f"{PREFIX}/reviews", response_model=ReviewResponse, status_code=201, tags=["Reviews"])
def create_review(data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # For simplicity, we won't check if the product exists
    new_review = Review(
        rating=data.rating,
        text=data.text,
        user_id=current_user.id,
        product_id=data.product_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@app.get(f"{PREFIX}/reviews", response_model=List[ReviewResponse], tags=["Reviews"])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
