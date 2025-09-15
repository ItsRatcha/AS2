#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Navigate to Django project directory
cd roombooking

# Try to run collectstatic, but continue if it fails
python manage.py collectstatic --noinput || echo "collectstatic failed, continuing..."

# Run migrations
python manage.py migrate

echo "Build completed successfully!"