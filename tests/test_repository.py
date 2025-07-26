import pytest

from app.database.repositories.secret_repository import SecretRepository
from app.models.schemas.secret import SecretCreate
from app.models.tables.secret import Secret

pytestmark = pytest.mark.asyncio(loop_scope='session')


async def test_create_and_get_secret(session_factory):
    """Тест создания и получения секрета"""
    db_session = session_factory()
    repo = SecretRepository(db_session)
    secret_data = SecretCreate(secret='secret', password='password')

    # Test create
    created_secret = await repo.create(obj_in=Secret.from_secret_create(secret_data))
    assert created_secret.id is not None
    assert created_secret.reg_date is not None
    assert created_secret.hashed_password is not None
    assert created_secret.secret is not None

    # Test get
    fetched_secret = await repo.get_by_id(created_secret.id)
    assert fetched_secret.id == created_secret.id
    assert fetched_secret.reg_date == created_secret.reg_date
    assert fetched_secret.hashed_password == created_secret.hashed_password
    assert fetched_secret.secret == created_secret.secret
    # Cleanup
    await db_session.commit()
