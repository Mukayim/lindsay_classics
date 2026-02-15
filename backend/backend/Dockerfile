# Build stage for frontend
FROM node:18 AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Final stage with Python
FROM python:3.11-slim
WORKDIR /app

# Debug: Show what's in the build context
RUN echo "=== Listing root directory contents ===" && ls -la /app || true

# Copy requirements.txt - this is the correct syntax
COPY backend/requirements.txt .

# Check if file was copied
RUN echo "=== Checking if requirements.txt was copied ===" && ls -la || true

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory
COPY backend/ ./backend/

# List contents after copy
RUN echo "=== Contents after copying backend ===" && ls -la /app/backend/

# Change to backend directory where manage.py is
WORKDIR /app/backend

# Check if manage.py exists
RUN echo "=== Checking for manage.py in /app/backend ===" && ls -la

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Start command
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT