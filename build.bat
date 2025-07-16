@echo off
echo Baresha Downloader - Building Executable
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install required dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the build script
echo Building executable...
python build_cross_platform.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Files created:
echo - dist/Baresha-Downloader.exe (The executable)
echo - install.bat (Installation script)
echo.
echo To install the application, run: install.bat
echo.
pause
