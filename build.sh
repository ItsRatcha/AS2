#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Navigate to Django project folder
cd roombooking

# Set environment variables
export DATABASE_URL=$DATABASE_URL

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"
