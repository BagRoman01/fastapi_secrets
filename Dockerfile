FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-cache

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY ./src ./src
COPY ./logging.yaml ./logging.yaml
COPY ./alembic.ini ./alembic.ini
COPY ./migrations ./migrations

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

CMD ["granian", "--interface", "asgi", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--log-level", "debug"]
