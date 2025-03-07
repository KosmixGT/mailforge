FROM python:3.12.2-slim

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=/app

# Install service dependencies
COPY services/delivery/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy service code
COPY services/delivery/app ./app
