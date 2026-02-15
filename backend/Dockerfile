FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory contents
COPY . .

# manage.py is in /app
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Start gunicorn - using exec form to avoid shell issues
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]