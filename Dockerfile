FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /test_project

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-cache-dir

COPY . .

# Остаёмся в /test_project, где лежит папка app
RUN chmod a+x docker_cmds/*.sh


