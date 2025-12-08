import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.injectors import acquire_services
from src.routers import api_router
from src.base.logger import setup_logging
from src.config import settings
from src.base.exceptions import register_exception_handlers

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    setup_logging()
    log.info("Application starting up...")
    async with acquire_services():
        yield

    log.info("Application shutting down...")


def setup_app() -> FastAPI:
    """Функция конфигурации приложения"""
    m_app = FastAPI(lifespan=lifespan)

    m_app.include_router(api_router)
    register_exception_handlers(m_app)

    m_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return m_app

app = setup_app()

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
