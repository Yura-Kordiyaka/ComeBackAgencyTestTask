FROM python:3.10

WORKDIR /app

RUN apt update && apt -qy upgrade

COPY ./requirements.txt app/requirements.txt

RUN pip install -r app/requirements.txt

COPY ./ /app/

WORKDIR /app/