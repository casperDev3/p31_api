from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Product
from schemas import ProductCreate, ProductResponse

import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="R&P 1104", version="0.4.0")


@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
