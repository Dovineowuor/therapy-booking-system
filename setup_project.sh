#!/bin/bash

# This script helps you set up the therapy booking system

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
echo "Creating a superuser for the admin panel..."
python manage.py createsuperuser

# Load sample data
echo "Loading sample data..."
python sample_data.py

# Run the server
echo "Starting the development server..."
python manage.py runserver 0.0.0.0:8000