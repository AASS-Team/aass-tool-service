# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /aass-tool-service

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pipenv dependencies
COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install
