FROM python:3.12.2-slim

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=/app

# Install shared package
COPY services/shared /shared
RUN pip install -e /shared

# Install service dependencies
COPY server/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy server code
COPY server/app ./app
