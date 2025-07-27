import logging

from fastapi import Depends

from app.core.security import decrypt_secret
from app.core.security import encrypt_secret
from app.core.security import verify_password
from app.models.schemas.secret import SecretCreate, SecretResponse
from app.models.schemas.secret import SecretWithData
from app.models.tables.secret import Secret
from app.services.exceptions.exceptions import ErrorDecryptSecretException, SecretNotFoundException
from app.services.exceptions.exceptions import WrongSecretPasswordException
from app.utils.uow import IUnitOfWork
from app.utils.uow import UnitOfWork
from app.models.schemas.secret import SecretUnlockPassword

logger = logging.getLogger(__name__)


class SecretService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_secret(self, *, create_secret: SecretCreate) -> SecretResponse:
        """Create new secret with given credentials.
        """
        async with self.uow as uow:
            create_secret.secret = encrypt_secret(
                create_secret.secret, create_secret.password,
            )
            s: Secret = Secret.from_secret_create(create_secret)
            new_secret = await uow.secret_repo.create(obj_in=s)
            res: SecretResponse = SecretResponse(reg_date=s.reg_date, id=s.id)
            await uow.commit()
            return res

    async def unsecret(self, secret_id: str, secret_data: SecretUnlockPassword) -> SecretWithData:
        async with self.uow as uow:
            secret = await uow.secret_repo.get_by_id(secret_id)
            if not secret:
                raise SecretNotFoundException
            if not verify_password(secret_data.password, secret.hashed_password):
                raise WrongSecretPasswordException
            data = SecretWithData(reg_date=secret.reg_date, secret=secret.secret)

            try:
                data.secret = decrypt_secret(secret.secret, secret_data.password)
            except Exception as e: 
                raise ErrorDecryptSecretException 
            
            await uow.secret_repo.delete(itm_id=secret.id)
            await uow.commit()
            return data


def get_secret_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> SecretService:
    return SecretService(uow)
