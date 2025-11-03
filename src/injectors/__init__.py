from fastapi import Depends
from src.database.repositories.secret_repository import SecretRepository
from src.injectors.pg import connection_injector
from src.injectors.repositories import repository_injector
from src.injectors.services import services_injector
from src.services.secret import SecretService

async def connection():
    async for session in connection_injector.get_session():
        yield session

def services(secret_service: SecretService = Depends(services_injector.get_secret_service)):
    return secret_service

def repository(secret_repo: SecretRepository = Depends(repository_injector.get_secret_repository)):
    return secret_repo
