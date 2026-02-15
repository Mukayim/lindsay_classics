# backend/Dockerfile (if placed in backend folder)
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/backend/requirements.txt

RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy project files (note the different path)
COPY . /app/

ENV PYTHONPATH=/app

RUN cd /app/backend && python manage.py collectstatic --noinput

EXPOSE $PORT

WORKDIR /app/backend

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT