from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.injectors.pg import connection_injector
from src.database.repositories.secret_repository import SecretRepository


class RepositoryInjector:
    def __init__(self, conn_injector):
        self.connection_injector = conn_injector

    def get_secret_repository(
        self,
        session: AsyncSession = Depends(connection_injector.get_session),
    ) -> SecretRepository:
        return SecretRepository(session)

repository_injector = RepositoryInjector(connection_injector)
