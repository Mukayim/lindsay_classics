# Dockerfile - place this file in the project root (lindsay/Dockerfile)

FROM python:3.13-slim

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Railway uses $PORT environment variable
ENV PORT=8080

# Set working directory to project root
WORKDIR /app

# Install system dependencies needed for psycopg and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the correct location (backend/requirements.txt)
COPY /backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the entire project
COPY . /app/

# Build React/Vite frontend (if the folder exists)
RUN if [ -d "/app/frontend" ]; then \
      cd /app/frontend && \
      npm install && \
      npm run build && \
      echo "Frontend build completed"; \
    else \
      echo "No frontend folder found — skipping frontend build"; \
    fi

# Collect static files — manage.py is in /app/backend/
RUN cd /app/backend && \
    python manage.py collectstatic --noinput --clear || \
    (echo "collectstatic failed — check manage.py exists in /app/backend" && exit 1)

# Expose the port Railway expects
EXPOSE $PORT

# Set working directory to the Django project folder for runtime
WORKDIR /app/backend

# Start Gunicorn
CMD ["gunicorn", "backend.wsgi:application", \
     "--bind", "0.0.0.0:$PORT", \
     "--workers", "4", \
     "--timeout", "120", \
     "--log-level", "info", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]