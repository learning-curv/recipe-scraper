FROM python:3.11-slim

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

