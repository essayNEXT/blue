# pull official base image
FROM python:3.11.2-slim-buster AS base

LABEL maintainer="Viktor Kyrychenko <vkir28@gmail.com>"

# ARG UID=1000
# ARG GID=1000
# ENV UID=${UID}
# ENV GID=${GID}

# RUN useradd -m -u $UID docker_user
# USER docker_user

# set work directory
WORKDIR /home/docker_user/app

# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN  pip install -r requirements.txt

# copy project
COPY . .

CMD ["python", "./django_project/manage.py", "runserver", "0.0.0.0:8000"]