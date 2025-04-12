FROM python:3.10-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8

RUN apt-get update && apt-get install -y \
    wget curl git unzip gnupg build-essential \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    libxss1 libasound2 libxshmfence1 libatk-bridge2.0-0 \
    libgtk-3-0 ca-certificates xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install langflow==1.3.2 playwright openai beautifulsoup4

RUN playwright install --with-deps chromium

EXPOSE 7860

WORKDIR /app

CMD ["langflow", "run", "--host", "0.0.0.0", "--port", "7860"]
