from sqlmodel import SQLModel, Field
from datetime import datetime

class SecretBase(SQLModel):
    reg_date: datetime | None = None


class SecretCreate(SQLModel):
    secret: str = Field(..., min_length=1, max_length=65536)
    password: str = Field(..., min_length=3, max_length=64)


class SecretPublicView(SecretBase):
    secret: str | None = None


class SecretInfo(SecretBase):
    id: str


class SecretUnlock(SQLModel):
    password: str = Field(..., min_length=3, max_length=64)
