import uuid

from pydantic import constr
from sqlmodel import SQLModel


def generate_uuid() -> str:
    return str(uuid.uuid4())


# Shared properties
class SecretBase(SQLModel):
    reg_date: str | None = None


class SecretCreate(SQLModel):
    secret: constr(min_length=1, max_length=65536)
    password: constr(min_length=3, max_length=64)


class SecretWithData(SecretBase):
    secret: str | None = None


class SecretUnlockData(SQLModel):
    id: str
    password: constr(min_length=3, max_length=64)
