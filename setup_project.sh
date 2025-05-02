#!/bin/bash

# This script helps you set up the therapy booking system

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database and apply migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Create a superuser
echo "Creating a superuser for the admin panel..."
python3 manage.py createsuperuser

# Load sample data
echo "Loading sample data..."
python3 sample_data.py

# Run the server
echo "Starting the development server..."
python3 manage.py runserver