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


