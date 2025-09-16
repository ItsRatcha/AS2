#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "DATABASE_URL is $DATABASE_URL"

# Check if manage.py exists
if [ -f "manage.py" ]; then
    echo "manage.py found! Running migrations..."
    python manage.py migrate --noinput
    python manage.py showmigrations
else
    echo "ERROR: manage.py not found!"
    echo "Current directory contents:"
    ls -la
    exit 1
fi

python manage.py collectstatic --noinput

echo "Build completed successfully!"