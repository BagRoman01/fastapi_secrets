import logging

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

log = logging.getLogger(__name__)

engine = create_async_engine(settings.ASYNC_DATABASE_URL)
log.info(f'Создаем engine с {settings.ASYNC_DATABASE_URL}')
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)
