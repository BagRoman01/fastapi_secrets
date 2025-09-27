import logging

from app.services.security import CryptoService
from app.services.security import crypto_service
from app.models.exceptions.exceptions import (
    SecretNotFoundException,
    WrongSecretPasswordException, \
    ErrorDecryptSecretException)
from app.models.schemas.secret import SecretCreate, SecretResponse
from app.models.schemas.secret import SecretWithData
from app.models.tables.secret import Secret
from app.base.uow import IUnitOfWork
from app.models.schemas.secret import SecretUnlockPassword

class SecretService:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow
        self._logger = logging.getLogger(__name__)
        self._crypto_service: CryptoService = crypto_service()

    async def create_secret(self, *, create_secret: SecretCreate) -> SecretResponse:
        """Create new secret with given credentials.
        """
        async with self._uow as uow:
            create_secret.secret = self._crypto_service.encrypt_secret(
                create_secret.secret, create_secret.password,
            )
            s: Secret = Secret.from_secret_create(create_secret)
            new_secret = await uow.secret_repo.create(obj_in=s)
            res: SecretResponse = SecretResponse(reg_date=s.reg_date, id=s.id)
            await uow.commit()
            return res

    async def unsecret(self, secret_id: str, secret_data: SecretUnlockPassword) -> SecretWithData:
        async with self._uow as uow:
            secret = await uow.secret_repo.get_by_id(secret_id)
            if not secret:
                raise SecretNotFoundException

            if not self._crypto_service.verify_password(secret_data.password, secret.hashed_password):
                raise WrongSecretPasswordException

            data = SecretWithData(reg_date=secret.reg_date, secret=secret.secret)

            try:
                data.secret = self._crypto_service.decrypt_secret(secret.secret, secret_data.password)
            except Exception as e: 
                raise ErrorDecryptSecretException 
            
            await uow.secret_repo.delete(itm_id=secret.id)
            await uow.commit()
            return data

