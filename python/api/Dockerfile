FROM python:3.7-alpine

ADD requirements.txt /code/api/requirements.txt

RUN apk --no-cache add --virtual build-dependencies \
      build-base \
      py-mysqldb \
      gcc \
      libc-dev \
      libffi-dev \
      mariadb-dev \
      && pip install -r /code/api/requirements.txt \
      && rm -rf .cache/pip \
      && apk del build-dependencies

RUN apk -q --no-cache add py-mysqldb

COPY . /code/api
WORKDIR /code/api

CMD honcho start -f /code/api/procfile $PROCESSES
