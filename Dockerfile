# Dockerfile - in repo root (lindsay/Dockerfile)

FROM python:3.13-slim

# Best practices for Django + Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system deps for psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from correct location
COPY backend\requirements.txt \app\backend\requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r \app\backend\requirements.txt

# Copy entire project
COPY . /app/

# Build frontend if folder exists
RUN if [ -d "/app/frontend" ]; then \
      cd /app/frontend && npm install && npm run build || echo "Frontend build failed/skipped"; \
    else \
      echo "No frontend folder - skipping build"; \
    fi

# Collect static files (manage.py is in /app/backend/)
RUN cd /app/backend && python manage.py collectstatic --noinput --clear || \
    (echo "collectstatic failed - check manage.py in /app/backend" && exit 1)

# Expose port Railway uses
EXPOSE $PORT

# Run Gunicorn from the Django project folder
WORKDIR /app/backend

CMD ["gunicorn", "backend.wsgi:application", \
     "--bind", "0.0.0.0:$PORT", \
     "--workers", "4", \
     "--timeout", "120", \
     "--log-level", "info", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]