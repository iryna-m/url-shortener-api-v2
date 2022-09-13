FROM python:3.8.1-alpine

# set working directory
WORKDIR /usr/src/shortener

# set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements.txt to working directory
COPY ./requirements.txt /usr/src/shortener/requirements.txt

# set dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project to Docker working directory
COPY . /usr/src/shortener/