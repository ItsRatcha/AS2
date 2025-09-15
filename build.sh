#!/usr/bin/env bash
set -o errexit

# Install Python dependencies from root requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Navigate to Django project directory
cd roombooking

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate

echo "Build completed successfully"