from datetime import datetime

from sqlmodel import Field

from app.core.security import get_password_hash
from app.models.schemas.secret import SecretBase
from app.models.schemas.secret import SecretCreate
from app.models.schemas.secret import generate_uuid


class Secret(SecretBase, table=True):
    id: str | None = Field(
        default_factory=generate_uuid, primary_key=True, index=True, nullable=False,
    )
    secret: str = Field(nullable=False, max_length=65536)
    hashed_password: str = Field(nullable=False, max_length=64)
    reg_date: str | None = Field(default=None)

    @staticmethod
    def from_secret_create(secret_create: SecretCreate) -> 'Secret':

        hashed_password = get_password_hash(secret_create.password)
        reg_date = str(datetime.now().isoformat())

        s = Secret(
            secret=secret_create.secret,
            hashed_password=hashed_password,
            reg_date=reg_date,
        )
        return s
