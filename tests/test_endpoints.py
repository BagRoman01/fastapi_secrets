import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio(loop_scope='session')


async def test_create_secret_success(async_client):
    """Тест успешного создания секрета"""
    payload = {'secret': 'my_secret', 'password': 'strong_password123'}
    response = await async_client.post('/generate', json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'id' in data
    assert 'reg_date' in data
    assert data['id'] is not None
    assert 'reg_date' is not None


async def test_create_secret_empty_secret(async_client):
    """Тест создания секрета с пустым содержимым"""
    payload = {'secret': '', 'password': 'pwd'}
    response = await async_client.post('/generate', json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert 'errors' in data
    assert any(
        e['loc'] == ['body', 'secret'] and e['type'] == 'string_too_short'
        for e in data['errors']
    )


async def test_create_secret_short_password(async_client):
    """Тест создания секрета с коротким паролем"""
    payload = {'secret': 'valid_secret', 'password': 'pw'}  # 2 символа
    response = await async_client.post('/generate', json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert 'errors' in data
    assert any(
        e['loc'] == ['body', 'password'] and e['type'] == 'string_too_short'
        for e in data['errors']
    )


async def test_unlock_secret_success(async_client):
    """Тест успешного открытия секрета"""
    # Сначала создаем секрет
    create_payload = {'secret': 'secret_to_unlock', 'password': 'unlock_pwd'}
    create_response = await async_client.post('/generate', json=create_payload)
    secret_id = create_response.json()['id']

    # Теперь открываем
    unlock_payload = {'id': secret_id, 'password': 'unlock_pwd'}
    response = await async_client.post(f'/unlock/{secret_id}', json=unlock_payload)
    print(response.json())

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['secret'] == 'secret_to_unlock'
    assert 'reg_date' in data


async def test_unlock_secret_not_found(async_client):
    """Тест открытия несуществующего секрета"""
    payload = {'id': '00000000-0000-0000-0000-000000000000', 'password': 'any_pwd'}
    response = await async_client.post(
        '/unlock/00000000-0000-0000-0000-000000000000', json=payload,
    )
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data.get('errors') == 'Secret with this id was not found!'


async def test_unlock_secret_wrong_password(async_client):
    """Тест открытия секрета с неверным паролем"""
    # Сначала создаем секрет
    create_payload = {'secret': 'protected_secret', 'password': 'correct_pwd'}
    create_response = await async_client.post('/generate', json=create_payload)
    secret_id = create_response.json()['id']

    # Пытаемся открыть с неверным паролем
    unlock_payload = {'id': secret_id, 'password': 'wrong_pwd'}
    response = await async_client.post(f'/unlock/{secret_id}', json=unlock_payload)
    data = response.json()

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert data.get('errors') == 'Wrong password for the secret!'


async def test_unlock_secret_twice(async_client):
    """Тест на невозможность повторного открытия секрета"""
    create_response = await async_client.post(
        '/generate', json={'secret': 'one_time_secret', 'password': 'pwd'},
    )
    secret_id = create_response.json()['id']

    # Первое успешное открытие
    first_unlock = await async_client.post(
        f'/unlock/{secret_id}', json={'id': secret_id, 'password': 'pwd'},
    )
    first_data = first_unlock.json()
    assert first_unlock.status_code == status.HTTP_200_OK
    assert first_data['secret'] == 'one_time_secret'

    # Повторная попытка — секрет уже удалён
    second_unlock = await async_client.post(
        f'/unlock/{secret_id}', json={'id': secret_id, 'password': 'pwd'},
    )
    second_data = second_unlock.json()
    assert second_unlock.status_code == status.HTTP_404_NOT_FOUND
    assert second_data.get('errors') == 'Secret with this id was not found!'
