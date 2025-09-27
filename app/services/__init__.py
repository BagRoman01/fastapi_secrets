from fastapi import Depends
from app.base.uow import UnitOfWork, IUnitOfWork
from app.services.secret import SecretService

def secret_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> SecretService:
    return SecretService(uow)


