#!/bin/bash

echo "YouTube Video Downloader"
echo "======================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 from your package manager"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
python3 -c "import yt_dlp, requests, PIL, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Run the application
echo "Starting YouTube Downloader..."
python3 youtube_downloader.py "$@" 