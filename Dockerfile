FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /fastapi_secrets

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-cache-dir --frozen --no-dev

ENV PATH="/fastapi_secrets/.venv/bin:$PATH"

COPY . .

WORKDIR /fastapi_secrets/src

CMD ["granian", "--interface", "asgi", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--log-level", "debug"]

