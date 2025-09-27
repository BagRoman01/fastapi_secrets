import logging
from abc import ABC
from abc import abstractmethod

from app.database.db_init import async_session_maker
from app.database.repositories.secret_repository import SecretRepository

log = logging.getLogger(__name__)


class IUnitOfWork(ABC):
    secret_repo: SecretRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.secret_repo = SecretRepository(self.session)
        log.debug('Создана новая сесия')
        # print("Создана новая сесия")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()
        log.debug('Закрытие сесии!')
        # print("Закрытие сесии!")

    async def rollback(self):
        await self.session.rollback()
        log.debug('Откат транзакции!')
        # print("Откат транзакции!")

    async def commit(self):
        await self.session.commit()
        log.debug('Подтверждение транзакции!')
        # print("Подтверждение транзакции!")
