from fastapi import Depends
from src.database.repositories import SecretRepository, secret_repository
from src.services.secret import SecretService

def secret_service(repo: SecretRepository = Depends(secret_repository)) -> SecretService:
    return SecretService(repo)


