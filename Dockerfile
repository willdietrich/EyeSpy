# syntax=docker/dockerfile:1

FROM python:3.11.11-slim-bullseye as builder

# Install pipenv
RUN pip install pipenv

# Set environment variables for pipenv
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app

# Copy Pipfile and Pipfile.lock for dependency installation
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11.11-slim-bullseye as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY eyespy ./eyespy

# Install system dependencies (sqlite3)
RUN apt-get update -y \
    && apt-get install -y sqlite3 \
    && mkdir /app/db \
    && /usr/bin/sqlite3 /app/db/eyespy.db

# Copy migration files and environment configuration
COPY alembic ./alembic
COPY alembic.ini .env main.py ./

# Run database migrations
RUN alembic upgrade head

ENTRYPOINT ["python", "main.py"]
