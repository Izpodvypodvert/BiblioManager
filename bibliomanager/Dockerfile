FROM python:3.10.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y wait-for-it
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
