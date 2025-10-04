# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app:create_app

WORKDIR /app

# Optional but handy for health checks, etc.
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install deps first (better layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY app ./app

EXPOSE 5000
# Simple start (good enough for staging). We'll swap to gunicorn later if you want.
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
