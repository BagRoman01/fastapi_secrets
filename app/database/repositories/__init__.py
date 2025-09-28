from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.repositories.secret_repository import SecretRepository
from app.database.db_init import get_session


def secret_repository(
    session: AsyncSession = Depends(get_session),
) -> SecretRepository:
    return SecretRepository(session)

