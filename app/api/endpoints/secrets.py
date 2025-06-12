from fastapi import APIRouter
from fastapi import Depends

from app.models.schemas.secret import SecretCreate
from app.models.schemas.secret import SecretUnlockData
from app.models.schemas.secret import SecretWithData
from app.models.tables.secret import Secret
from app.services.secret import SecretService
from app.services.secret import get_secret_service

router = APIRouter()


@router.post('/unlock/{id}', response_model=SecretWithData)
async def unsecret(
    secret_service: SecretService = Depends(get_secret_service),
    *,
    secret_unlock: SecretUnlockData,
) -> SecretWithData:
    """Reads the secret and then deletes it.
    """
    return await secret_service.unsecret(secret_unlock)


@router.post('/generate', response_model=Secret)
async def create_secret(
    *,
    secret_service: SecretService = Depends(get_secret_service),
    secret_create: SecretCreate,
) -> Secret:
    """Create new secret with given credentials.
    """
    return await secret_service.create_secret(create_secret=secret_create)
