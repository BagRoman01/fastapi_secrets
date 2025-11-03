import logging

from src.database.repositories.secret_repository import SecretRepository
from src.services.security import CryptoService
from src.base.exceptions import (
    SecretNotFoundException,
    WrongSecretPasswordException, \
    ErrorDecryptSecretException)
from src.models.schemas.secret import SecretCreate, SecretInfo
from src.models.schemas.secret import SecretPublicView
from src.models.tables.secret import Secret
from src.models.schemas.secret import SecretUnlock

class SecretService:
    def __init__(self, repo: SecretRepository, crypto: CryptoService):
        self._logger = logging.getLogger(__name__)
        self._crypto_service: CryptoService = crypto
        self._secret_repository: SecretRepository = repo

    async def create_secret(
            self,
            *,
            create_secret: SecretCreate
    ) -> SecretInfo:
        """Create new secret with given credentials.
        """
        create_secret.secret = self._crypto_service.encrypt_secret(
            create_secret.secret, create_secret.password,
        )
        s: Secret = Secret.from_create(create_secret)
        new_secret = await self._secret_repository.create(obj_in=s)
        res: SecretInfo = SecretInfo(reg_date=s.reg_date, id=s.id)
        await self._secret_repository.db.commit()
        return res

    async def unsecret(
            self,
            secret_id: str,
            secret_data: SecretUnlock
    ) -> SecretPublicView:
        secret = await self._secret_repository.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundException

        if not self._crypto_service.verify_password(secret_data.password,
                                                    secret.hashed_password):
            raise WrongSecretPasswordException

        data = SecretPublicView(reg_date=secret.reg_date, secret=secret.secret)

        try:
            data.secret = self._crypto_service.decrypt_secret(
                secret.secret,
                secret_data.password)
        except Exception as e:
            raise ErrorDecryptSecretException

        await self._secret_repository.delete(itm_id=secret.id)
        await self._secret_repository.db.commit()
        return data

