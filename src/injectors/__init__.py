from functools import lru_cache
from src.injectors.pg import AsyncPgConnectionInj
from src.injectors.services import (
    AsyncServiceInjector,
    CryptoServiceInjector
)

@lru_cache(maxsize=1)
def acquire_connections() -> AsyncPgConnectionInj:
    return AsyncPgConnectionInj()

@lru_cache(maxsize=1)
def acquire_crypto() -> CryptoServiceInjector:
    return CryptoServiceInjector()

@lru_cache(maxsize=1)
def acquire_services(
        conns: AsyncPgConnectionInj | None = None,
        crypto: CryptoServiceInjector | None = None,
) -> AsyncServiceInjector:
    conns = conns or acquire_connections()
    crypto = crypto or acquire_crypto()

    return AsyncServiceInjector(
        conns_inj=conns,
        crypto_inj=crypto,
    )
