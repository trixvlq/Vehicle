FROM python:3.10-alpine

RUN apk add postgresql-client build-base postgresql-dev

COPY requirements.txt /temp/requirements.txt

RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY . /backend

WORKDIR /backend

RUN adduser --disabled-password postgres-user

USER postgres-user

EXPOSE 8000