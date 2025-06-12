import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.repositories.base_repository import BaseRepository
from app.models.schemas.secret import SecretCreate
from app.models.tables.secret import Secret

logger = logging.getLogger(__name__)


class SecretRepository(BaseRepository[Secret, SecretCreate, SecretCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Secret, session)
