FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system deps for Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from correct location
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project
COPY . /app/

# Build frontend if folder exists
RUN if [ -d "frontend" ]; then \
      cd frontend && npm install && npm run build || echo "Frontend build skipped"; \
    else \
      echo "No frontend folder - skipping build"; \
    fi

# Collect static files (manage.py is in /app/backend/)
RUN cd backend && python manage.py collectstatic --noinput --clear || \
    (echo "collectstatic failed - check manage.py in /app/backend" && exit 1)

EXPOSE $PORT

WORKDIR /app/backend

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:$PORT", "--workers", "4", "--timeout", "120", "--log-level", "info"]