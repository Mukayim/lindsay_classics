FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend folder
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy everything
COPY . /app/

# Build frontend if it exists
RUN if [ -d "/app/frontend" ]; then \
      cd /app/frontend && npm install && npm run build || echo "Frontend build skipped"; \
    else \
      echo "No frontend folder - skipping build"; \
    fi

# Collect static – from the folder that has manage.py
RUN cd /app/backend && python manage.py collectstatic --noinput --clear || \
    (echo "collectstatic failed - check if manage.py exists in /app/backend" && exit 1)

EXPOSE $PORT

# Run from the Django project folder
WORKDIR /app/backend

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:$PORT", "--workers", "4", "--timeout", "120", "--log-level", "info"]