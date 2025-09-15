#!/usr/bin/env bash
# Exit on error
set -o errexit

# Python dependencies only
python -m pip install --upgrade pip
pip install -r requirements.txt

# Django setup
python manage.py collectstatic --noinput
python manage.py migrate

echo "Build completed successfully"