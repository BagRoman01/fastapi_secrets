import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import settings

log = logging.getLogger(__name__)


class ConnectionInjector:
    def __init__(self) -> None:
        self.engine = create_async_engine(settings.ASYNC_DATABASE_URL)
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.async_session_maker() as session:
            yield session

connection_injector = ConnectionInjector()