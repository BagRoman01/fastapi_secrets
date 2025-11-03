from src.database.repositories.secret_repository import SecretRepository
from src.injectors.repositories import repository_injector
from src.services.security import CryptoService
from src.services.secret import SecretService
from fastapi import Depends

class ServiceInjector:
    def __init__(self):
        self.crypto_service = CryptoService()

    async def get_secret_service(
        self,
        secret_repo: SecretRepository = Depends(repository_injector.get_secret_repository),
    ) -> SecretService:
        return SecretService(secret_repo, self.crypto_service)

services_injector = ServiceInjector()
