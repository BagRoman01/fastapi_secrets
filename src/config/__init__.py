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

    DATABASE_HOST: str = 'postgres'
    DATABASE_PORT: int = 5432
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'db'

    CORS_ORIGINS: list[str] = ['*']

    HOST: str = '0.0.0.0'
    PORT: int = 8000

    def __init__(self, **kwargs):
        env = os.getenv('APP_MODE', 'dev')
        print("РЕЖИМ: " + env)
        env_files = [f'../../.env.{env}', f'../.env.{env}', f'.env.{env}']
        super().__init__(
            **kwargs,
            _env_file=env_files,
            _env_file_encoding='utf-8'
        )

def load_settings() -> Settings:
    """Загружает настройки с проверкой валидности"""
    try:
        return Settings()
    except ValidationError as e:
        print('ОШИБКА: Неверная конфигурация приложения!')
        print('Проверьте файл .env или переменные окружения:')
        for error in e.errors():
            field = error['loc'][0]
            msg = error['msg']
            print(f"  - {field}: {msg}")
        raise ValueError("Конфигурация приложения невалидна") from e
    except Exception as e:
        print(f'ОШИБКА: Не удалось загрузить конфигурацию: {e}')
        raise ValueError("Не удалось инициализировать настройки") from e


settings = load_settings()


