FROM python:3.12.5-slim

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./reqs/ ./reqs

RUN pip install -r ./reqs/requirements.txt

COPY . ./