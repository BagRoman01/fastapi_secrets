from fastapi import APIRouter

from src.routers import secrets

api_router = APIRouter()
api_router.include_router(secrets.router, prefix='/secret', tags=['secret'])
