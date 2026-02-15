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

# Copy backend requirements (path is correct now - from root)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory
COPY backend/ ./backend/

# Copy built frontend to Django's static directory (adjust path based on your frontend build output)
COPY --from=frontend-build /frontend/dist /app/backend/static/

# Set working directory to where manage.py is
WORKDIR /app/backend/backend

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start command
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT