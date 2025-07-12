@echo off
echo YouTube Video Downloader
echo ======================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import yt_dlp, requests, PIL, tkinter, sv_ttk" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if FFmpeg is installed locally
if not exist "ffmpeg\ffmpeg.exe" (
    echo Installing FFmpeg...
    python install_ffmpeg.py
    if errorlevel 1 (
        echo Warning: FFmpeg installation failed, but downloader will still work
    )
)

REM Run the application
echo Starting YouTube Downloader...
python youtube_downloader.py %*

pause 