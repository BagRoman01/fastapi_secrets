from typing import AsyncGenerator, Any
from src.injectors.pg import AsyncPgConnectionInj
from src.services import SecretService, CryptoService

class AsyncServiceInjector:
    def __init__(self, conns: AsyncPgConnectionInj):
        self.crypto_service = CryptoService()
        self._conns = conns

    async def secrets(self) -> AsyncGenerator[SecretService, Any]:
        async with self._conns.acquire_session() as session:
            yield SecretService(session, self.crypto_service)
