# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System packages (minimal); add build tools if needed
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata and sources
COPY pyproject.toml README.zebras.md alembic.ini ./
COPY src ./src
COPY docs ./docs
COPY migrations ./migrations

# Install
RUN pip install --upgrade pip && pip install .

# Runtime env (override via compose/env)
ENV ZEBRAS_HTTP_HOST=0.0.0.0 \
    ZEBRAS_HTTP_PORT=43117 \
    LOG_LEVEL=INFO

# Entrypoint selects mode and runs migrations first
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 43117

ENTRYPOINT ["/entrypoint.sh"]
