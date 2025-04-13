FROM python:3.10-slim

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ffmpeg \
    build-essential \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libxrandr2 \
    xdg-utils \
    wget \
    libu2f-udev \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    libatk-bridge2.0-0 \
    libgtk-3-0 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install chromium

