#!/bin/bash

# This script helps you push the therapy booking system to your GitHub repository

# Check if GitHub username is provided
if [ -z "$1" ]; then
  echo "Please provide your GitHub username as the first argument"
  echo "Usage: ./setup_github.sh your_github_username [repository_name]"
  exit 1
fi

GITHUB_USERNAME=$1

# Set repository name (default or provided)
REPO_NAME=${2:-therapy-booking-system}

# Configure remote repository
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

echo "Remote repository configured as: https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo ""
echo "Before pushing, please create a repository named '$REPO_NAME' on your GitHub account."
echo ""
echo "Then push your code with:"
echo "git push -u origin main"
echo ""
echo "If you want to push the feature branch instead:"
echo "git push -u origin django-therapy-booking"