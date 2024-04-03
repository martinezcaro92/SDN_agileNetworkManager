# pull official base image
FROM python:3.11.0-alpine

# set work directory
WORKDIR /usr/src/mocks

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
# COPY ./requirements.txt /usr/src/app/requirements.txt

# copy project
COPY . /usr/src/mocks/

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
         openssl-dev libffi-dev gcc musl-dev python3-dev bash \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/mocks/requirements.txt \
    && rm -rf /root/.cache/pip


