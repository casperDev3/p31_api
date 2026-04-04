from fastapi import FastAPI, HTTPException, Depends, Request
from typing import Optional, List
import time
from pydantic import BaseModel
from functools import wraps
from datetime import datetime
import uvicorn
import re

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

    @staticmethod
    def get_sorted_by_price(sort: str, products: List[ProductModel]) -> List[ProductModel]:
        if sort == "asc":
            return sorted(products, key=lambda x: x.price)
        elif sort == "desc":
            return sorted(products, key=lambda x: x.price, reverse=True)
        else:
            raise ValueError("Invalid sort parameter. Use 'asc' or 'desc'.")

    def filter_by_price(self, filter_lt: Optional[float] = None, filter_gt: Optional[float] = None) -> List[
        ProductModel]:
        filtered_products = self._db
        if filter_lt is not None:
            filtered_products = [p for p in filtered_products if p.price < filter_lt]
            if not filtered_products:
                raise ValueError("No products found with price less than the specified value.")
        if filter_gt is not None:
            filtered_products = [p for p in filtered_products if p.price > filter_gt]
            if not filtered_products:
                raise ValueError("No products found with price greater than the specified value.")
        return filtered_products

    @staticmethod
    def get_filtered(filters: dict, products: List[ProductModel]) -> List[ProductModel]:
        for field, conditions in filters.items():
            for operator, value in conditions.items():
                if operator == "lt":
                    products = [p for p in products if getattr(p, field) < float(value)]
                elif operator == "gt":
                    products = [p for p in products if getattr(p, field) > float(value)]
                elif operator == "eq":
                    products = [p for p in products if getattr(p, field) == float(value)]
                else:
                    raise ValueError(f"Unsupported operator: {operator}")
        return products


repo = ProductRepository()


def get_db_session():
    print("-> Opening DB session")
    try:
        yield repo
    finally:
        print("-> Closing DB session")

def parse_filters(request: Request) -> dict:
    filters = {}
    pattern = re.compile(r"^filters\[(.*?)]\[(.*?)]$")

    for key, value in request.query_params.items():
        match = pattern.match(key)
        if match:
            field = match.group(1)
            operator = match.group(2)

            if field not in filters:
                filters[field] = {}
            filters[field][operator] = value
    return filters

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/health")
@log_execution_time
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get(f"{API_PREFIX}/products", response_model=List[ProductModel])
@log_execution_time
async def get_products(
        sort: Optional[str] = None,
        filters: dict = Depends(parse_filters),
):
    try:
        print(filters)
        products = repo.get_all_products()
        if filters:
            products = repo.get_filtered(filters, products)
        if sort:
            products = repo.get_sorted_by_price(sort, products)
        return products
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(f"{API_PREFIX}/products/{{product_id}}", response_model=ProductModel)
@log_execution_time
async def get_product(
        product_id: int,
        db: ProductRepository = Depends(get_db_session)
):
    product = db.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
