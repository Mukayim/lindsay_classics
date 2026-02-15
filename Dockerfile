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

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend to Django's static directory
COPY --from=frontend-build /frontend/dist /app/backend/backend/static/

WORKDIR /app/backend/backend
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT