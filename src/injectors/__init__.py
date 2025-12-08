from functools import lru_cache
from src.injectors.pg import AsyncPgConnectionInj
from src.injectors.services import ServiceInjector

@lru_cache(maxsize=1)
def acquire_connections() -> AsyncPgConnectionInj:
    return AsyncPgConnectionInj()

@lru_cache(maxsize=1)
def acquire_services(
        conns: AsyncPgConnectionInj | None = None
) -> ServiceInjector:
    conns = conns or acquire_connections()

    return ServiceInjector(
        conns_inj=conns
    )

