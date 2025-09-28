#!/bin/bash

echo "🔧 BEGIN Running alembic migrations..."
uv run alembic upgrade head

echo "✅ BEGIN Running tests..."
uv run pytest -s -v

echo "🚀 Starting server..."
uv run gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level debug \
  --access-logfile - \
  --error-logfile -