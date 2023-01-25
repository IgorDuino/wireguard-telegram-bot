FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt

COPY . .
