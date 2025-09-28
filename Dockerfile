FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /fastapi_secrets

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-cache-dir

COPY . .

# Остаёмся в /test_project, где лежит папка src
RUN chmod a+x docker_cmds/*.sh


