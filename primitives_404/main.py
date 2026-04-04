from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
import time
from pydantic import BaseModel
from functools import wraps
from datetime import datetime
import uvicorn

# ----- 1. Constants -----
API_PREFIX = "/api/v1"
DEFAULT_CURRENCY = "UAH"

app = FastAPI(title="Welcome FastAPI", version="0.0.1")


# ----- 2. Decorators -----
def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")
        return result

    return wrapper


# ----- 3. OOP -----
# 1. Encapsulation | 2. Polymorphism | 3. Inheritance | 4. Abstraction
class ProductModel(BaseModel):
    id: int
    name: str
    price: float


class ProductRepository:
    def __init__(self):
        self._db: List[ProductModel] = [
            ProductModel(id=1, name="Ноутбук", price=45000.0),
            ProductModel(id=2, name="Смартфон", price=25000.0),
            ProductModel(id=3, name="Навушники", price=4000.0),
        ]

    def get_all_products(self) -> List[ProductModel]:
        return self._db

    def get_product_by_id(self, product_id: int) -> ProductModel | None:
        return next((item for item in self._db if item.id == product_id), None)

    def get_sorted_by_price(self, sort: str) -> List[ProductModel]:
        if sort == "asc":
            return sorted(self._db, key=lambda x: x.price)
        elif sort == "desc":
            return sorted(self._db, key=lambda x: x.price, reverse=True)
        else:
            raise ValueError("Invalid sort parameter. Use 'asc' or 'desc'.")


repo = ProductRepository()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/health")
@log_execution_time
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get(f"{API_PREFIX}/products", response_model=List[ProductModel])
@log_execution_time
async def get_products(sort: Optional[str] = None):
    if sort:
        try:
            return repo.get_sorted_by_price(sort)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    return repo.get_all_products()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
