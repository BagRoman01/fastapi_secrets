from typing import List

from pydantic import ValidationError
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=['../../.env', '../.env', '.env'],
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
    )

    # DATABASE GROUP
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_USER: str
    DATABASE_PASS: str
    DATABASE_NAME: str

    CORS_ORIGINS: list[str] | str

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str):
            return [url.strip().rstrip('/') for url in v.split(',') if url]
        return None

    # DEPLOYMENT GROUP
    DEPLOY_HOST: str
    DEPLOY_PORT: int

    @property
    def ASYNC_DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASS}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'


try:
    settings = Settings()
except ValidationError as e:
    print('Ошибка в настройках. Проверьте .env файл или переменные окружения:')
    print(e.errors())  # Детальный список ошибок
