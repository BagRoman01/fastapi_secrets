from fastapi import APIRouter
from fastapi import Depends

from app.models.schemas.secret import (
    SecretUnlockPassword,
    SecretWithData,
    SecretCreate,
    SecretResponse
)
from app.services.secret import SecretService
from app.services.__init__ import secret_service

router = APIRouter()


@router.post('/unlock/{secret_id}')
async def unsecret(
    secret_id: str,  # получаем id из URL
    secret_unlock: SecretUnlockPassword,  # тело запроса содержит только пароль
    secret_srv: SecretService = Depends(secret_service),
) -> SecretWithData:
    """Reads the secret and then deletes it."""
    return await secret_srv.unsecret(
        secret_id=secret_id,
        secret_data=SecretUnlockPassword(password=secret_unlock.password)
    )


@router.post('/generate')
async def create_secret(
    *,
    secret_srv: SecretService = Depends(secret_service),
    secret_create: SecretCreate,
) -> SecretResponse:
    """Create new secret with given credentials."""
    return await secret_srv.create_secret(create_secret=secret_create)
