# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app:create_app

WORKDIR /app

# Install deps first (better cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Your code is at repo root; copy it into /app/app so it becomes a package named "app"
COPY . ./app

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
