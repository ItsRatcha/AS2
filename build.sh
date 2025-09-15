#!/usr/bin/env bash
# Exit on error
set -o errexit

npm install
npm run build:css

# Modify this line as needed for your project
python -m pip install --upgrade pip

pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply any outstanding migrations
python manage.py migrate