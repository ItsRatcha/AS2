#!/usr/bin/env bash
# Exit on error
set -o errexit

# Python dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Node.js dependencies (only if package.json exists)
if [ -f package.json ]; then
    echo "Installing Node.js dependencies..."
    npm install
    npm run build:css
fi

# Django setup
python manage.py collectstatic --noinput
python manage.py migrate