from fastapi import APIRouter, Depends
from src.injectors import acquire_services
from src.models import (
    SecretUnlock,
    SecretPublicView,
    SecretCreation,
    SecretInfo
)
from src.services import SecretService

router = APIRouter()

@router.post('/{secret_id}/unlock')
async def unsecret(
    secret_id: str,
    secret_unlock: SecretUnlock,
    secret_srv: SecretService = Depends(acquire_services().secrets),
) -> SecretPublicView:
    """Reads the secret and then deletes it."""
    return await secret_srv.unsecret(
        secret_id=secret_id,
        secret_data=SecretUnlock(password=secret_unlock.password)
    )


@router.post('')
async def create_secret(
    secret_create: SecretCreation,
    secret_srv: SecretService = Depends(acquire_services().secrets),
) -> SecretInfo:
    """Create new secret with given credentials."""
    return await secret_srv.create_secret(secret_creation=secret_create)
