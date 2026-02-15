FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

# DEBUG: show folder contents
RUN echo "Listing /app:" && ls -la /app
RUN echo "Listing /app/backend:" && ls -la /app/backend || echo "backend folder missing"
RUN echo "manage.py exists?" && ls -la /app/backend/manage.py || echo "manage.py NOT FOUND"

# Try collectstatic
RUN cd /app/backend && python manage.py collectstatic --noinput || echo "collectstatic failed"

EXPOSE $PORT

WORKDIR /app/backend

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:$PORT", "--workers", "4", "--timeout", "120", "--log-level", "info"]