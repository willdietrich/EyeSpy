# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apt-get update -y  \
    && apt install -y sqlite3 \
    && /usr/bin/sqlite3 /app/db/eyespy.db

COPY . .

RUN alembic upgrade head

CMD ["python3", "main.py" ]
