import os
from typing import List
from pydantic import ValidationError
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
    )

    # поля
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_USER: str
    DATABASE_PASS: str
    DATABASE_NAME: str

    CORS_ORIGINS: List[str] | str

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [url.strip().rstrip('/') for url in v.split(',') if url]
        return v

    DEPLOY_HOST: str
    DEPLOY_PORT: int

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.DATABASE_USER}:{self.DATABASE_PASS}'
            f'@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
        )

    def __init__(self, **kwargs):
        # читаем режим из переменной окружения
        env = os.getenv('APP_MODE', 'dev')  # dev, test или prod
        print("РЕЖИМ: " + env)
        # список файлов: сначала специфичный, потом общий
        env_files = [f'../../.env.{env}', f'../.env.{env}', f'.env.{env}']
        # передаём его родителю
        super().__init__(**kwargs, _env_file=env_files, _env_file_encoding='utf-8')


try:
    # os.environ['APP_MODE'] = 'test'
    settings = Settings()
except ValidationError as e:
    print('Ошибка в настройках. Проверьте файл или переменные окружения:')
    print(e.errors())  # Детальный список ошибок
