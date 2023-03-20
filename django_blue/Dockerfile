FROM python:alpine3.17
LABEL maintainer="Onyshchenko Serhii"
ARG UID=1000
ARG GID=1000
ENV UID=${UID}
ENV GID=${GID}
RUN useradd -m -u $UID docker_user
USER docker_user

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN  pip install -r requirements.txt
COPY . .

