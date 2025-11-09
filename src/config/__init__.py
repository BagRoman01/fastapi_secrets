import os
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
    )

    DATABASE_HOST: str
    DATABASE_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    CORS_ORIGINS: list[str]

    DEPLOY_HOST: str
    DEPLOY_PORT: int

    def __init__(self, **kwargs):
        env = os.getenv('APP_MODE', 'dev')
        print("РЕЖИМ: " + env)
        env_files = [f'../../.env.{env}', f'../.env.{env}', f'.env.{env}']
        super().__init__(**kwargs, _env_file=env_files,
                         _env_file_encoding='utf-8')


try:
    settings = Settings()
except ValidationError as e:
    print('Ошибка в настройках. Проверьте файл или переменные окружения:')
    print(e.errors())
