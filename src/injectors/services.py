from typing import AsyncGenerator, Any
from src.injectors.pg import AsyncPgConnectionInj
from src.services import SecretService, CryptoService

class CryptoServiceInjector:
    def __init__(self):
        self._crypto_service = CryptoService()

    def get_crypto_service(self) -> CryptoService:
        return self._crypto_service

class AsyncServiceInjector:
    def __init__(
            self,
            conns_inj: AsyncPgConnectionInj,
            crypto_inj: CryptoServiceInjector
    ):
        self._conns = conns_inj
        self._crypto_inj = crypto_inj

    async def __aenter__(self) -> 'AsyncServiceInjector':
        """Инициализация подключений при старте приложения"""
        await self._conns.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Устранение подключений"""
        if self._conns:
            await self._conns.disconnect()
        return False

    async def secrets(self) -> AsyncGenerator[SecretService, Any]:
        if not self._conns:
            raise RuntimeError("Connections not initialized")
        async with self._conns.acquire_session() as session:
            yield SecretService(
                session,
                self._crypto_inj.get_crypto_service()
            )
