#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install required packages
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

export DJANGO_SUPERUSER_USERNAME=junction
export DJANGO_SUPERUSER_EMAIL=junction@gmail.com
export DJANGO_SUPERUSER_PASSWORD=Junction@123

# Create superuser if it doesn't exist
python <<EOF
import os
from decouple import config

from django.contrib.auth import get_user_model
User = get_user_model()



username = os.getenv("DJANGO_SUPERUSER_USERNAME", "junction")
email = os.getenv"DJANGO_SUPERUSER_EMAIL", "junction@gmail.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "Junction@123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
EOF