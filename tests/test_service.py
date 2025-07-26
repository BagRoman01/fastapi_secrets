import pytest
from pydantic import ValidationError

from app.models.schemas.secret import SecretCreate
from app.models.schemas.secret import SecretUnlockData
from app.services.exceptions.exceptions import SecretNotFoundException
from app.services.exceptions.exceptions import WrongSecretPasswordException

pytestmark = pytest.mark.asyncio(loop_scope='session')


async def test_empty_secret_create(secret_service):
    """Тест на попытку создания пустого секрета"""
    with pytest.raises(ValidationError) as exc_info:
        secret = await secret_service.create_secret(
            create_secret=SecretCreate(secret='', password='pwd'),
        )
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == ('secret',)
    assert errors[0]['type'] == 'string_too_short'
    assert errors[0]['msg'] == 'String should have at least 1 character'


async def test_short_password_create(secret_service):
    """Тест проверяет, что пароль короче 3 символов вызывает ValidationError"""
    with pytest.raises(ValidationError) as exc_info:
        await secret_service.create_secret(
            create_secret=SecretCreate(
                secret='valid_secret', password='pw',
            ),  # 2 символа
        )

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == ('password',)
    assert errors[0]['type'] == 'string_too_short'
    assert errors[0]['msg'] == 'String should have at least 3 characters'


async def test_create_secret(secret_service, test_uow):
    """Тест на создание секрета"""
    secret = await secret_service.create_secret(
        create_secret=SecretCreate(secret='secret', password='pwd'),
    )

    async with test_uow as uow:
        new_secret = await uow.secret_repo.get_by_id(secret.id)
        assert new_secret is not None, 'Секрет не был создан!'


async def test_unsecret_id_not_found(secret_service):
    """Тест проверяет вызов SecretNotFoundException при попытке открыть несуществующий секрет"""
    with pytest.raises(SecretNotFoundException):
        await secret_service.unsecret(
            SecretUnlockData(
                id='00000000-0000-0000-0000-000000000000', password='any_pwd',
            ),
        )


async def test_unsecret_with_wrong_password(secret_service, test_uow):
    """Тест проверяет вызов WrongSecretPasswordException при неверном пароле"""
    # Сначала создаем секрет
    secret = await secret_service.create_secret(
        create_secret=SecretCreate(secret='secret', password='correct_pwd'),
    )

    # Пытаемся открыть с неверным паролем
    with pytest.raises(WrongSecretPasswordException):
        await secret_service.unsecret(
            SecretUnlockData(id=secret.id, password='wrong_pwd'),
        )

    # Проверяем, что секрет остался в БД (не удалился при неверном пароле)
    async with test_uow as uow:
        existing_secret = await uow.secret_repo.get_by_id(secret.id)
        assert (
            existing_secret is not None
        ), 'Секрет не должен удаляться при неверном пароле'


async def test_unlock_secret(secret_service, test_uow):
    """Тест на правильность открытия секрета"""
    secret = await secret_service.create_secret(
        create_secret=SecretCreate(secret='new_secret', password='my_pwd'),
    )
    assert secret is not None, 'Секрет не был создан'
    data = await secret_service.unsecret(
        SecretUnlockData(id=secret.id, password='my_pwd'),
    )
    assert data is not None, 'Получены пустые данные при открытии секрета'
    assert (
        data.reg_date == secret.reg_date
    ), 'Даты регистрации секрета при создании и после разблокировки не совпали!'
    assert data.secret == 'new_secret', 'Содержимое секрета разблокировано неверно!'

    async with test_uow as uow:
        deleted_secret = await uow.secret_repo.get_by_id(secret.id)
        assert deleted_secret is None, 'Секрет не был удалён после разблокировки!'
