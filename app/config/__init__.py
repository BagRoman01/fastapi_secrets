import os
from typing import List
from pydantic import ValidationError
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
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    CORS_ORIGINS: List[str]

    DEPLOY_HOST: str
    DEPLOY_PORT: int

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.POSTGRES_DB}'
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
