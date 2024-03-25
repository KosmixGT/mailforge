# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
