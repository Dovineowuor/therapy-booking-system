#!/bin/bash

# Install dependencies
pip install -r requirements.txt django-cors-headers

# Apply migrations
python manage.py migrate

# Load sample data
python sample_data.py

# Run the server with proper settings for iframe and CORS
export DJANGO_ALLOW_ASYNC_UNSAFE=true
export DJANGO_SETTINGS_MODULE=therapy_project.settings
python manage.py runserver 0.0.0.0:12000 --insecure