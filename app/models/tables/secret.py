from datetime import datetime
import uuid
from sqlmodel import Field
from app.models.schemas.secret import SecretBase
from app.models.schemas.secret import SecretCreate
from app.services.security import crypto_service


class Secret(SecretBase, table=True):
    id: str | None = Field(
        default_factory=lambda: str(str(uuid.uuid4())), primary_key=True, index=True, nullable=False,
    )
    secret: str = Field(nullable=False, max_length=65536)
    hashed_password: str = Field(nullable=False, max_length=64)
    reg_date: str | None = Field(default=None)

    @staticmethod
    def from_secret_create(secret_create: SecretCreate) -> 'Secret':

        hashed_password = crypto_service().hash_password(secret_create.password)
        reg_date = str(datetime.now().isoformat())

        s = Secret(
            secret=secret_create.secret,
            hashed_password=hashed_password,
            reg_date=reg_date,
        )
        return s