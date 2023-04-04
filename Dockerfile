FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

