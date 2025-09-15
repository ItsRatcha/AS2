#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Navigate to Django project folder
cd roombooking

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"
