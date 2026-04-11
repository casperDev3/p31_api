from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    text = Column(String, nullable=True)
    role = Column(String, default="user")  # "user" or "admin"

    # 1 user have many reviews
    reviews = relationship("Reviews", back_populates="owner")
    products = relationship("Products", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)

    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"))

    # 1 product have many reviews
    reviews = relationship("Reviews", back_populates="product")

class Reviews(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer) # 1-5
    text = Column(String, nullable=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # Relationships
    owner = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")