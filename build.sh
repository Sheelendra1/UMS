#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

cd ums
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser automatically
# You can change these values or remove these lines after the first successful login
export DJANGO_SUPERUSER_PASSWORD='Admin@123'
python manage.py createsuperuser --no-input --username admin --email admin@example.com || true
