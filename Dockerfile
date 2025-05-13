FROM python:3.11.12-alpine3.20

RUN apk add build-base

RUN apk add postgresql-dev gcc python3-dev musl-dev

ARG FLASK_APP
ARG FLASK_ENV
ARG DATABASE_URL
ARG SCHEMA
ARG SECRET_KEY

ENV DATABASE_URL=$DATABASE_URL
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install psycopg2

COPY . .

RUN flask db upgrade
CMD ["flask","run"]
