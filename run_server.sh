#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Load sample data
python sample_data.py

# Run the server
python manage.py runserver 0.0.0.0:12000