from fastapi import FastAPI
import uvicorn
from routers import auth, users

PREFIX = "/api/v1"

app = FastAPI(title="Restructured FastAPI App", version="0.3.0")

app.include_router(auth.router, prefix=PREFIX)
app.include_router(users.router, prefix=PREFIX)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)