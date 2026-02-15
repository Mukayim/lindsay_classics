FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

# DEBUG COPY
RUN echo "=== DEBUG: Listing /app/backend ===" && ls -la /app/backend || echo "backend folder missing"
RUN echo "=== DEBUG: manage.py check ===" && ls -la /app/backend/manage.py || echo "manage.py NOT FOUND"

# Collect static
RUN cd /app/backend && python manage.py collectstatic --noinput --clear || echo "collectstatic failed"

EXPOSE $PORT

WORKDIR /app/backend

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:$PORT", "--workers", "4", "--timeout", "120", "--log-level", "info"]