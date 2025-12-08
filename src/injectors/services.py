from typing import AsyncGenerator, Any
from src.injectors.pg import AsyncPgConnectionInj
from src.services import SecretService, CryptoService

class ServiceInjector:
    def __init__(
            self,
            conns_inj: AsyncPgConnectionInj,
    ):
        self._conns = conns_inj

    async def __aenter__(self) -> 'ServiceInjector':
        """Инициализация подключений при старте приложения"""
        await self._conns.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Устранение подключений"""
        if self._conns:
            await self._conns.disconnect()
        return False

    @staticmethod
    def get_crypto_service() -> CryptoService:
        return CryptoService()

    async def secrets(self) -> AsyncGenerator[SecretService, Any]:
        if not self._conns:
            raise RuntimeError("Connections not initialized")
        async with self._conns.acquire_session() as session:
            yield SecretService(
                session,
                self.get_crypto_service()
            )
