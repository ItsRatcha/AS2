#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Navigate to Django project folder
cd roombooking

# Run migrations first
python manage.py migrate --noinput || echo "migrate failed, continuing..."

# Collect static files
python manage.py collectstatic --noinput || echo "collectstatic failed, continuing..."

# Start gunicorn server with the correct WSGI path
gunicorn <roombooking>.wsgi:application --bind 0.0.0.0:10000
