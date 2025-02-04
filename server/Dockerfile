FROM python:3.12.2-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
