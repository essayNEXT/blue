FROM python:3.11.2-alpine

LABEL maintainer="Yulia Panaseiko <Yulia.nishtayulia@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN pip install 'piccolo[postgres]'

WORKDIR /piccolo_blue

COPY . .
