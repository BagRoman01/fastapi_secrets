import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime
from src.services.security import CryptoService


class SecretBase(SQLModel):
    reg_date: datetime | None = None


class SecretCreation(SQLModel):
    secret: str = Field(..., min_length=1, max_length=65536)
    password: str = Field(..., min_length=3, max_length=64)


class SecretPublicView(SecretBase):
    secret: str | None = None


class SecretInfo(SecretBase):
    id: str


class SecretUnlock(SQLModel):
    password: str = Field(..., min_length=3, max_length=64)


class Secret(SecretBase, table=True):
    id: str | None = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
    )
    secret: str = Field(nullable=False, max_length=65536)
    hashed_password: str = Field(nullable=False, max_length=64)
    reg_date: str | None = Field(default=None)

    @classmethod
    def from_create(cls, secret_create: SecretCreation) -> 'Secret':

        hashed_password = CryptoService().hash_password(
            secret_create.password
        )
        reg_date = str(datetime.now().isoformat())

        s = Secret(
            secret=secret_create.secret,
            hashed_password=hashed_password,
            reg_date=reg_date,
        )
        return s