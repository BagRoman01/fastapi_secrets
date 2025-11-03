from fastapi import APIRouter
from fastapi import Depends

from src.models.schemas.secret import (
    SecretUnlock,
    SecretPublicView,
    SecretCreate,
    SecretInfo
)
from src.services.secret import SecretService
from src.injectors.__init__ import services

router = APIRouter()


@router.post('/{secret_id}/unlock')
async def unsecret(
    secret_id: str,
    secret_unlock: SecretUnlock,
    secret_srv: SecretService = Depends(services),
) -> SecretPublicView:
    """Reads the secret and then deletes it."""
    return await secret_srv.unsecret(
        secret_id=secret_id,
        secret_data=SecretUnlock(password=secret_unlock.password)
    )


@router.post('')
async def create_secret(
    *,
    secret_srv: SecretService = Depends(services),
    secret_create: SecretCreate,
) -> SecretInfo:
    """Create new secret with given credentials."""
    return await secret_srv.create_secret(create_secret=secret_create)
