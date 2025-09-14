from fastapi import FastAPI
from app.api_routes import router as api_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="RideWise API")

app.include_router(api_router, prefix="/api")

if not os.path.exists("data"):
    os.makedirs("data")

@app.get("/")
async def root():
    return {"message": "RideWise backend. Use /api endpoints."}
