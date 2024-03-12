# syntax=docker/dockerfile:1

FROM python:3.10-buster as builder

RUN pip install poetry==1.7.0

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.10-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY eyespy ./eyespy

RUN apt-get update -y  \
    && apt install -y sqlite3 \
    && mkdir /app/db \
    && /usr/bin/sqlite3 /app/db/eyespy.db

COPY alembic ./alembic
COPY alembic.ini .env ./
RUN alembic upgrade head

WORKDIR eyespy

ENTRYPOINT ["python", "-m", "main"]
