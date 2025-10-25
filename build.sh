#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt

cd roombooking

# Set environment variables
export DATABASE_URL=$DATABASE_URL

echo "DATABASE_URL is $DATABASE_URL"

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"
else
    echo "Superuser environment variables not set, skipping superuser creation"
fi

echo "Running migrations..."
python manage.py migrate --noinput


echo "Installing Tailwind dependencies..."
cd theme/static_src
npm install
npm run build
cd ../..

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"


