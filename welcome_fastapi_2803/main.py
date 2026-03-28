from fastapi import FastAPI
from datetime import datetime
import uvicorn

app = FastAPI(title="Welcome FastAPI", version="0.0.1")

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
