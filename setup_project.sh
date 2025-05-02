#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Cleaning up migration files (except __init__.py)..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

echo "Cleaning up .pyc files..."
find . -path "*/migrations/*.pyc" -delete

echo "Cleaning up __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -r {} +

echo "Cleaning up virtual environment directories..."

# Function to remove a directory if it exists
remove_dir_if_exists() {
    if [[ -d "$1" ]]; then
        rm -rf "$1"
        echo "$1 directory removed."
    else
        echo "$1 directory does not exist."
    fi
}

# Deactivate the virtual environment if active
if [[ -n "$VIRTUAL_ENV" ]]; then
    if command -v deactivate &> /dev/null; then
        deactivate
    else
        echo "No virtual environment to deactivate."
    fi
fi

# Check and remove env, venv, and .venv directories
remove_dir_if_exists "env"
remove_dir_if_exists "venv"
remove_dir_if_exists ".venv"

echo "Installing virtualenv..."
python3 -m virtualenv .venv

echo "Activating virtualenv..."
source .venv/bin/activate

echo "Installing requirements..."
pip install --upgrade -r requirements.txt

echo "Migration cleanup and cache cleanup completed."

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Migration completed."

# echo "Cleaning up cache..."
# python manage.py clear_cache

# Create self-signed SSL certificate if it doesn't exist
echo "Checking for SSL certificate..."
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    echo "Creating self-signed SSL certificate..."
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes << EOF
    
EOF
    echo "SSL certificate created."
else
    echo "SSL certificate already exists."
fi


# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run Django development server with insecure flag
echo "Running Django development server..."
python manage.py runserver 0.0.0.0:8000 --insecure

echo "Server started."

echo "Done."
