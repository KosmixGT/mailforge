FROM python:3.12.2-slim

RUN apt-get update && apt-get install -y libpq-dev

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=/app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
