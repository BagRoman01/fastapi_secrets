# tests/test_uow.py

import pytest

from app.models.schemas.secret import SecretCreate
from app.models.tables.secret import Secret

pytestmark = pytest.mark.asyncio(loop_scope='session')


async def test_uow_commit(test_uow):
    """Тестирование коммита uow"""
    async with test_uow as uow:
        new_secret = SecretCreate(secret='my_secret', password='PASSWORD')
        secret = await uow.secret_repo.create(
            obj_in=Secret.from_secret_create(new_secret),
        )
        await uow.commit()

    async with test_uow as uow:
        result = await uow.secret_repo.get_by_id(itm_id=secret.id)
        assert result is not None

    async with test_uow as uow:
        res = await uow.secret_repo.delete(itm_id=secret.id)
        await uow.commit()

    async with test_uow as uow:
        result = await uow.secret_repo.get_by_id(itm_id=secret.id)
        assert result is None


async def test_uow_rollback(test_uow):
    """Тестирование отката uow"""
    async with test_uow as uow:
        new_secret = SecretCreate(secret='my_secret', password='PASSWORD')
        secret = await uow.secret_repo.create(
            obj_in=Secret.from_secret_create(new_secret),
        )

    async with test_uow as uow:
        result = await uow.secret_repo.get_by_id(itm_id=secret.id)
        assert result is None
