FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

WORKDIR /app

# Install system dependencies for PostgreSQL & Pillow
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Render port
EXPOSE 10000

# Run migrations, seed database, and start Gunicorn on dynamic Render PORT
CMD ["sh", "-c", "python manage.py migrate --noinput && python populate_db.py && gunicorn apex_project.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers 2"]
