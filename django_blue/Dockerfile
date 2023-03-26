# pull official base image
FROM python:alpine3.17 AS base
LABEL maintainer="Onyshchenko Serhii"

# set work directory
WORKDIR /usr/src/app

# Забороняє записувати файли .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Забороняє Python буферизувати stdout и stderr
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN  pip install -r requirements.txt
# copy project
COPY . .

