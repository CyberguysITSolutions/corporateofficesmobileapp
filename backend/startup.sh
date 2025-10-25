#!/bin/bash
# Azure App Service startup script

# Navigate to app directory
cd /home/site/wwwroot

# Install dependencies if not already installed
if [ ! -d "venv" ]; then
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run database migrations (first deployment only)
# Uncomment the following line after first deployment
# python init_db.py

# Start Gunicorn
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 4 app:app
