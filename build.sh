#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Check if we're in the right directory and run migrations
if [ -f "manage.py" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput
    echo "Migrations completed"
else
    echo "ERROR: manage.py not found in current directory!"
    echo "Looking for manage.py..."
    find . -name "manage.py" -type f
    exit 1
fi

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"