from fastapi import APIRouter

from src.api.endpoints import secrets

api_router = APIRouter()
api_router.include_router(secrets.router, prefix='/secrets', tags=['secrets'])
