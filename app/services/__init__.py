from fastapi import Depends
from app.database.repositories import SecretRepository, secret_repository
from app.services.secret import SecretService

def secret_service(repo: SecretRepository = Depends(secret_repository)) -> SecretService:
    return SecretService(repo)


