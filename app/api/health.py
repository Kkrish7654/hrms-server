# app/api/health.py
from fastapi import APIRouter
from app.core.response import success

router = APIRouter()

@router.get("/health")
async def health_check():
    return success(data={"status": "healthy"}, message="Application is running smoothly")
