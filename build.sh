#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files with WhiteNoise
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Seed database with initial products, categories, reviews and superuser
python populate_db.py
