import logging
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routers import api_router
from src.base.logger import setup_logging
from src.config import settings
from src.base.exceptions import register_exception_handlers

setup_logging()
log = logging.getLogger(__name__)
app = FastAPI()
app.include_router(api_router)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
