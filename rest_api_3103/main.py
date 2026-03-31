from functools import wraps
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Generator
from datetime import datetime
import uvicorn

app = FastAPI(title="REST FastAPI", version="0.0.1")

def log_execution_time(endpoint_name: str):
    def decorator(func):
        # TODO: next lesson
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = await func(*args, **kwargs)
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            print(f"Endpoint '{endpoint_name}' executed in {execution_time:.4f} seconds")
            return result
        return wrapper
    return decorator

# models #TODO: next lesson
class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class User(UserCreate):
    id: int


# local db
users_db: List[User] = []
user_id_counter = 1

#TODO: next lesson
def user_id_generator() -> Generator[int, None, None]:
    global user_id_counter
    while True:
        yield user_id_counter
        user_id_counter += 1

id_gen = user_id_generator()

# lambda filters #TODO: next lesson
filter_adults = lambda users: [user for user in users if user.age >= 18]
filter_by_name = lambda name: lambda users: [user for user in users if user.name.lower() == name.lower()]

# 404
def get_user_or_404(user_id: int) -> User:
    user = next((user for user in users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# users
@app.post("/users/", response_model=User)
@log_execution_time("create_user")
async def create_user(user: UserCreate):
    try:
        new_user = User(
            id=next(id_gen),
            **user.model_dump()
        )
        users_db.append(new_user)
        return new_user
    except Exception as e:
        # return 400 with error message
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[User])
@log_execution_time("list_users")
async def get_all_users():
    return users_db


# @app.get("/users/{user_id}", response_model=User)
# @log_execution_time("get_user")
# async def get_user(user: User = Depends(get_user_or_404)):
#     return user

@app.get("/users/{user_id}", response_model=User)
@log_execution_time("get_user")
async def get_user(user_id: int):
    return get_user_or_404(user_id)

# @app.delete("/users/{user_id}")
# @log_execution_time("delete_user")
# async def delete_user(user: User = Depends(get_user_or_404)):
#     users_db.remove(user)
#     return {"message": f"User with id {user.id} deleted successfully"}

@app.delete("/users/{user_id}", response_model=User)
@log_execution_time("delete_user")
async def delete_user(user_id: int):
    user = get_user_or_404(user_id)
    users_db.remove(user)
    return user





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)