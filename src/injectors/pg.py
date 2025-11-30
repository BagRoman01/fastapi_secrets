import asyncio
import logging
import os
from contextlib import asynccontextmanager
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database
import typing as t
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    async_scoped_session
)
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import settings
from alembic.config import Config as AlembicConfig
from alembic import command

class AsyncPgConnectionInj:
    def __init__(self) -> None:
        self._session_factory = None
        self._engine = None
        self._logger = logging.getLogger(__name__)
        self._is_setup = False

    def _build_url(self, async_driver=True) -> URL:
        driver = 'postgresql+asyncpg' if async_driver else 'postgresql'
        return URL.create(
            driver,
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            database=settings.POSTGRES_DB,
        )

    async def init_db(self) -> None:
        """Проверка и создание базы данных, если не существует."""
        try:
            sync_url = self._build_url(False)
            if not database_exists(sync_url):
                create_database(sync_url)
                self._logger.info("База данных создана.")
            else:
                self._logger.debug("База данных уже существует.")
        except Exception as e:
            self._logger.warning(
                "Не удаётся найти/создать базу данных.",
                extra={"e": e}
            )

    async def _create_engine(self) -> AsyncEngine:
        """Создание движка"""
        return create_async_engine(self._build_url())

    async def _run_alembic_upgrade(self) -> None:
        """Применение миграций Alembic"""
        self._logger.info("Применение миграций Alembic...")

        try:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(
                os.path.join(
                    cur_dir,
                    os.pardir,
                    os.pardir
                )
            )
            alembic_ini_path = os.path.join(project_root, "alembic.ini")
            alembic_cfg = AlembicConfig(alembic_ini_path)
            command.upgrade(alembic_cfg, "head")
            self._logger.info("Миграции успешно применены.")
        except Exception as e:
            self._logger.error(
                "Ошибка при применении миграций Alembic.",
                extra={"e": e}
            )
            raise e

    async def setup(self) -> None:
        """Инициализация подключения к БД."""
        if self._is_setup:
            return

        try:
            await self.init_db()
            self._engine = await self._create_engine()
            await self._run_alembic_upgrade()

            async_session_maker = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

            self._session_factory = async_scoped_session(
                async_session_maker,
                scopefunc=asyncio.current_task
            )

            self._is_setup = True
            self._logger.info(
                f'PostgreSQL подключение создано.',
                extra={
                    'host': settings.DATABASE_HOST,
                    'port': settings.DATABASE_PORT,
                    'database': settings.POSTGRES_DB,
                }
            )

        except Exception as e:
            self._logger.error(
                f"Ошибка при создании PostgreSQL подключения: {e}",
                exc_info=True
            )
            raise

    @asynccontextmanager
    async def acquire_session(self) -> t.AsyncGenerator[AsyncSession, None]:
        """Получение сессии БД с автоматическим управлением."""
        if not self._is_setup:
            await self.setup()

        if not self._session_factory:
            raise RuntimeError('Не удалось создать фабрику сессий')

        try:
            async with self._session_factory() as session:
                yield session
        except Exception as e:
            self._logger.exception("Ошибка сессии базы данных")
            raise

    async def disconnect(self) -> None:
        """Закрытие всех подключений."""
        try:
            if self._session_factory:
                await self._session_factory.remove()
                self._session_factory = None

            if self._engine:
                await self._engine.dispose()
                self._engine = None

            self._is_setup = False
            self._logger.info('PostgreSQL подключение успешно закрыто')

        except Exception as e:
            self._logger.warning(
                f'Внимание: Ошибка при отключении соединения PostgreSQL',
                extra={'e': e},
            )

        return self._is_setup and self._engine is not None