#!/bin/bash
# Production startup script

echo "Starting YouTube API Production System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start cookie extractor in background
echo "Starting cookie extractor..."
python youtube_cookie_extractor.py &

# Start main application
echo "Starting main application..."
gunicorn --bind 0.0.0.0:5000 --workers 2 main:app
