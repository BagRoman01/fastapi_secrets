
from app.config import Settings


def test_settings_successful_creation():
    """Тест успешного создания экземпляра Settings"""
    settings = Settings()

    # Assert
    assert settings.DATABASE_HOST == 'db'
    assert settings.DATABASE_PORT == '5432'
    assert settings.POSTGRES_USER == 'postgres'
    assert settings.POSTGRES_PASSWORD == 'postgres'
    assert settings.POSTGRES_DB == 'test_db'
    assert settings.CORS_ORIGINS == ['http://localhost:3000', 'http://PRODUCTION.example.com']
    assert settings.DEPLOY_HOST == '127.0.0.1'
    assert settings.DEPLOY_PORT == 8000
    assert settings.ASYNC_DATABASE_URL == (
        'postgresql+asyncpg://postgres:postgres@db:5432/test_db'
    )
