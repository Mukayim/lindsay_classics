FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory contents
COPY . .

# List files to debug
RUN echo "=== Files in /app ===" && ls -la
RUN echo "=== Files in /app/backend ===" && ls -la /app/backend || echo "No /app/backend directory"

# manage.py is in /app, not /app/backend
# Run migrations from /app where manage.py is
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Start gunicorn - point to the nested backend.wsgi
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT