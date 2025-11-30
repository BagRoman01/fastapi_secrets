from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.services import CryptoService
from src.base import (
    SecretNotFoundException,
    WrongSecretPasswordException,
    ErrorDecryptSecretException
)
from src.models import (
    SecretCreation,
    SecretInfo,
    Secret,
    SecretPublicView,
    SecretUnlock
)

class SecretService:
    def __init__(self, session: AsyncSession, crypto: CryptoService):
        self._crypto_service: CryptoService = crypto
        self._db = session

    async def create_secret(
            self,
            secret_creation: SecretCreation
    ) -> SecretInfo:
        """Создание нового секрета с паролем."""
        secret_creation.secret = self._crypto_service.encrypt_secret(
            secret_creation.secret,
            secret_creation.password
        )
        s: Secret = Secret.from_create(secret_creation)
        self._db.add(s)
        await self._db.flush()
        await self._db.refresh(s)
        await self._db.commit()
        res: SecretInfo = SecretInfo(reg_date=s.reg_date, id=s.id)
        return res

    async def unsecret(
            self,
            secret_id: str,
            secret_data: SecretUnlock
    ) -> SecretPublicView:
        """Раскрытие секрета по его ID и паролю"""
        result = await self._db.exec(
            select(Secret).where(Secret.id == secret_id)
        )
        secret = result.one_or_none()

        if not secret:
            raise SecretNotFoundException

        if not self._crypto_service.verify_password(
                secret_data.password,
                secret.hashed_password
        ):
            raise WrongSecretPasswordException

        data = SecretPublicView(
            reg_date=secret.reg_date,
            secret=secret.secret
        )

        try:
            data.secret = self._crypto_service.decrypt_secret(
                secret.secret,
                secret_data.password
            )
        except Exception as e:
            raise ErrorDecryptSecretException

        await self._db.delete(secret)
        await self._db.commit()

        return data

