from functools import lru_cache
from src.injectors.pg import AsyncPgConnectionInj
from src.injectors.services import AsyncServiceInjector

def acquire_connections() -> AsyncPgConnectionInj:
    return AsyncPgConnectionInj()

@lru_cache
def acquire_services(
        conns: AsyncPgConnectionInj | None = None,
) -> AsyncServiceInjector:
    conns = conns or acquire_connections()

    return AsyncServiceInjector(
        conns=conns
    )
