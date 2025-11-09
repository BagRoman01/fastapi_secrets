FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /fastapi_secrets

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-cache-dir

COPY . .

# Остаёмся в /test_project, где лежит папка src
RUN uv run gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level debug \
  --access-logfile - \
  --error-logfile -


