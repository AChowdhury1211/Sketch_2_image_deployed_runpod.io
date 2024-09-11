FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libsndfile1 \
    libsndfile1-dev \
    ffmpeg \
    git \
    apt-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000

COPY . /app/

RUN pip install runpod

CMD ["python3.10", "-u", "src/handler.py"]