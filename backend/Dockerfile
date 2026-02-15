FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory contents
COPY . .

# Move to the nested backend directory where manage.py is
WORKDIR /app/backend

# Run migrations and collect static files
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Start gunicorn
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT