FROM python:3.11.2-alpine

LABEL maintainer="Yulia Panaseiko <Yulia.nishtayulia@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

#COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install 'piccolo[postgres]'

# Инициализация проекта
WORKDIR /piccolo_blue

COPY . .
#RUN adduser -D user

#USER user