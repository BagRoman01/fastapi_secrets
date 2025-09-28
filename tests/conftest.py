import httpx
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main import app
from src.models.schemas.secret import SecretBase
from src.services.secret import SecretService
from src.base.uow import UnitOfWork


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def async_engine():
    """Фикстура для создания асинхронного движка (на всю сессию тестов)"""
    # Используем тестовую БД (можно использовать SQLite в памяти для тестов)
    test_db_url = 'sqlite+aiosqlite:///:memory:'

    engine = create_async_engine(test_db_url, connect_args={'check_same_thread': False})

    # Создаем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(SecretBase.metadata.create_all)

    # Проверка подключения
    async with engine.begin() as conn:
        try:
            # Простой тестовый запрос
            result = await conn.execute(text('SELECT 1'))
            # assert result.scalar() == 1
            print(f'\nУспешное подключение к базе данных {result.scalar()}')
        except Exception as e:
            pytest.fail(f'Не удалось подключиться к базе данных: {e!s}')

    yield engine

    # Удаляем все таблицы после завершения тестов
    async with engine.begin() as conn:
        await conn.run_sync(SecretBase.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def session_factory(async_engine):
    return async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False,
    )


@pytest_asyncio.fixture(loop_scope='session')
async def test_uow(session_factory):
    class TestUnitOfWork(UnitOfWork):
        def __init__(self):
            self.session_factory = session_factory
            super().__init__()

    return TestUnitOfWork()


@pytest_asyncio.fixture(loop_scope='session')
async def secret_service(test_uow):
    return SecretService(test_uow)


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def async_client():
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(
        transport=transport, base_url='http://127.0.0.1:8000/secrets',
    ) as async_client:
        yield async_client
