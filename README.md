# 🔐 Сервис одноразовых секретов (FastAPI + PostgreSQL)

REST API-сервис для безопасного хранения и одноразовой передачи секретов.  
Секрет можно создать с кодовой фразой и получить одноразовый код для его последующего просмотра.

## 📦 Возможности

- Создание секрета с кодовой фразой
- Генерация одноразового кода доступа
- Один просмотр секрета по коду, после чего он удаляется
- Документация Swagger/OpenAPI

---

### 🧱 Архитектура приложения

* **🔄 UoW (Unit of Work)** – паттерн, инкапсулирующий все операции с базой данных в пределах одного запроса. Это упрощает управление транзакциями и откатами при ошибках.
* **📦 Repository Pattern** – паттерн, обеспечивающий абстракцию доступа к данным. Репозитории скрывают детали работы с ORM и позволяют легко подменять реализацию или писать тесты.

🧩 Использование этих паттернов позволяет:

* изолировать бизнес-логику от слоя хранения данных;
* повысить тестируемость;
* централизованно управлять транзакциями;
* проще следовать принципам SOLID.

---

## 🧱 Стек технологий

### ⚙️ Backend

* **[FastAPI](https://fastapi.tiangolo.com/)** – современный веб-фреймворк на Python для создания высокопроизводительных REST API
* **[SQLAlchemy](https://www.sqlalchemy.org/)** / **[SQLModel](https://sqlmodel.tiangolo.com/)** – ORM и декларативная работа с моделями
* **[Pydantic v2](https://docs.pydantic.dev/)** – валидация и сериализация данных
* **[Alembic](https://alembic.sqlalchemy.org/)** – миграции схемы базы данных
* **[Asyncpg](https://github.com/MagicStack/asyncpg)** – высокопроизводительный асинхронный драйвер PostgreSQL
* **[Aiosqlite](https://github.com/omnilib/aiosqlite)** – асинхронный драйвер для SQLite (используется при тестировании)

### 🔒 Безопасность

* **[Passlib](https://passlib.readthedocs.io/)** + **[bcrypt](https://pypi.org/project/bcrypt/)** – безопасное хеширование паролей
* **[Cryptography](https://cryptography.io/)** – криптографические функции и шифрование

### 🧪 Тестирование

* **[Pytest](https://docs.pytest.org/)** – фреймворк для написания тестов
* **[Pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)** – поддержка асинхронных тестов
* **[Httpx](https://www.python-httpx.org/)** – асинхронный HTTP-клиент, используется для тестов API

### 🚀 Запуск и деплой

* **[Uvicorn](https://www.uvicorn.org/)** – быстрый ASGI-сервер для разработки
* **[Gunicorn](https://gunicorn.org/)** – сервер для продакшн-развёртывания
* **[Docker + Docker Compose](https://docs.docker.com/compose/)** – контейнеризация приложения и БД
* **[uv](https://github.com/astral-sh/uv)** – современный и быстрый менеджер зависимостей (альтернатива pip)

### 🧹 Статический анализ и стиль кода

* **[Ruff](https://docs.astral.sh/ruff/)** – сверхбыстрый линтер и автоформаттер Python-кода
* **[Mypy](https://mypy-lang.org/)** – проверка типов на основе аннотаций
* **[Black](https://black.readthedocs.io/)** – автоформаттер для кода с чётким стилевым стандартом

---

## 🚀 Быстрый старт (Docker)

1. Клонируй репозиторий:

- git clone https://github.com/BagRoman01/secrets.git

2. Создай `.env` файл (пример ниже) или используй уже существующий.

3. Построй и запусти сервис:

- docker compose up --build

4. Открой API-документацию:

* Swagger UI: [http://localhost:8000/docs]
  
---

## ⚙️ Переменные окружения (`.env`)

```env
# DATABASE
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASS=postgres
DATABASE_NAME=test_db

# FRONTEND COMMUNICATION
CORS_ORIGINS=http://localhost:3000,http://PRODUCTION.example.com

# DEPLOYMENT
DEPLOY_HOST=127.0.0.1
DEPLOY_PORT=8000
```

---

## 🐘 Структура `docker-compose.yml`

* `db` — PostgreSQL 15 с проверкой готовности.
* `app` — FastAPI-приложение на Python 3.12.

---

## 📦 Примеры API

### 🔐 Создание секрета

`POST /generate`

Создаёт одноразовый секрет и возвращает уникальный код для его получения.
На секрет и пароль наложены ограничения:
    secret: constr(min_length=1, max_length=65536)
    password: constr(min_length=3, max_length=64)

#### 🔸 Пример запроса:

```json
{
  "secret": "secret",
  "password": "parol"
}
```

#### 🔸 Пример ответа:

```json
{
  "reg_date": "2025-07-26T18:33:42.099375",
  "secret": "fcdaa0dba711b55e20925072ec1a34dd674141414141426f68522d46745534626730714a74513765386574394a697269735a47482d6d7975696c6b685a6956665f55683161456a5752796934325568743471364a375f31476b324b7670496e77705339424f6e7974645156474f364e6679413d3d",
  "hashed_password": "$2b$12$FY0rvglUqiRSV7K.lYmcuetPyM6e4i3ptb141CUzCGkRxdKByMheS",
  "id": "260b98ba-4b80-45e3-ab5f-7f5f6f16bd4b"
}
```

---
### 📥 Получение и удаление секрета

`POST /unlock/{id}`

Позволяет один раз прочитать ранее созданный секрет. После этого он удаляется.

#### 🔸 Пример запроса:

```json
{
  "id": "260b98ba-4b80-45e3-ab5f-7f5f6f16bd4b",
  "password": "parol"
}
```

#### 🔸 Пример ответа:

```json
{
  "reg_date": "2025-07-26T18:33:42.099375",
  "secret": "secret"
}
```

#### ⚠️ Повторный доступ:

Если тот же `code` использовать повторно — будет ошибка `404 Not Found`, потому что секрет уже удалён.
```json
{
  "errors": "Secret with this id was not found!"
}
```
