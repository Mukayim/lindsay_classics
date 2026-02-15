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

# Copy requirements.txt from backend folder (it's directly in backend, not in a subfolder)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory
COPY backend/ ./backend/

# Copy built frontend to Django's static directory
COPY --from=frontend-build /frontend/dist /app/backend/static/

# The manage.py is in /app/backend/, not /app/backend/backend/
WORKDIR /app/backend

# Run collectstatic (manage.py is here)
RUN python manage.py collectstatic --noinput

# For gunicorn, we need to point to the nested backend folder's wsgi
# The wsgi.py is at /app/backend/backend/wsgi.py
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --chdir /app/backend