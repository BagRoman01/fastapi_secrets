from fastapi import APIRouter
from fastapi import Depends

from app.models.schemas.secret import SecretCreate, SecretResponse, SecretUnlockPassword
from app.models.schemas.secret import SecretWithData
from app.models.tables.secret import Secret
from app.services.secret import SecretService
from app.services.secret import get_secret_service

router = APIRouter()


@router.post('/unlock/{id}', response_model=SecretWithData)
async def unsecret(
    id: str,  # получаем id из URL
    secret_unlock: SecretUnlockPassword,  # тело запроса содержит только пароль
    secret_service: SecretService = Depends(get_secret_service),
) -> SecretWithData:
    """Reads the secret and then deletes it."""
    return await secret_service.unsecret(secret_id=id, secret_data=SecretUnlockPassword(password=secret_unlock.password))



@router.post('/generate', response_model=SecretResponse)
async def create_secret(
    *,
    secret_service: SecretService = Depends(get_secret_service),
    secret_create: SecretCreate,
) -> SecretResponse:
    """Create new secret with given credentials."""
    return await secret_service.create_secret(create_secret=secret_create)
