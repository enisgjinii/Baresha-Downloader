#!/usr/bin/env python3
"""
Cross-platform build script for creating executables from YouTube Video Downloader
Supports Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def get_platform_info():
    """Get current platform information."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "windows", "exe"
    elif system == "darwin":
        return "macos", "app"
    elif system == "linux":
        return "linux", "bin"
    else:
        return "unknown", "bin"

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyInstaller: {e}")
            return False

def create_spec_file(platform_name, extension):
    """Create a PyInstaller spec file for the application."""
    
    # Platform-specific configurations
    platform_configs = {
        "windows": {
            "console": False,
            "icon": "baresha-logo.jpg",
            "datas": [
                ('baresha-logo.jpg', '.'),
                ('ffmpeg', 'ffmpeg'),
                ('install_ffmpeg.py', '.'),
            ]
        },
        "macos": {
            "console": False,
            "icon": "baresha-logo.jpg",
            "datas": [
                ('baresha-logo.jpg', '.'),
                ('ffmpeg', 'ffmpeg'),
                ('install_ffmpeg.py', '.'),
            ],
            "codesign_identity": None,
            "entitlements_file": None,
        },
        "linux": {
            "console": False,
            "icon": "baresha-logo.jpg",
            "datas": [
                ('baresha-logo.jpg', '.'),
                ('ffmpeg', 'ffmpeg'),
                ('install_ffmpeg.py', '.'),
            ]
        }
    }
    
    config = platform_configs.get(platform_name, platform_configs["linux"])
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['youtube_downloader.py'],
    pathex=[],
    binaries=[],
    datas={config["datas"]},
    hiddenimports=[
        'yt_dlp',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'requests',
        'urllib.request',
        'urllib.parse',
        'json',
        'datetime',
        'collections',
        'threading',
        'subprocess',
        'pathlib',
        'time',
        're',
        'sys',
        'os',
        'sv_ttk',
        'darkdetect',
        'pystray',
        'plyer',
        'plyer.notification',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Baresha-Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={config["console"]},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity={config.get("codesign_identity", "None")},
    entitlements_file={config.get("entitlements_file", "None")},
    icon='{config["icon"]}',
)
'''
    
    spec_filename = f'Baresha-Downloader-{platform_name}.spec'
    with open(spec_filename, 'w') as f:
        f.write(spec_content)
    print(f"Created PyInstaller spec file: {spec_filename}")
    return spec_filename

def build_executable(platform_name, extension):
    """Build the executable using PyInstaller."""
    print(f"Building executable for {platform_name}...")
    
    # Create spec file
    spec_filename = create_spec_file(platform_name, extension)
    
    # Build the executable
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            spec_filename
        ])
        print(f"Executable built successfully for {platform_name}!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build executable for {platform_name}: {e}")
        return False

def create_installer_scripts(platform_name, extension):
    """Create installer scripts for the current platform."""
    
    if platform_name == "windows":
        # Windows installer
        installer_content = '''@echo off
echo Baresha Downloader - Installer
echo ==============================

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\\Baresha-Downloader
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "dist\\Baresha-Downloader.exe" "%INSTALL_DIR%\\"

REM Create desktop shortcut
set DESKTOP=%USERPROFILE%\\Desktop
echo @echo off > "%DESKTOP%\\Baresha-Downloader.bat"
echo start "" "%INSTALL_DIR%\\Baresha-Downloader.exe" >> "%DESKTOP%\\Baresha-Downloader.bat"

REM Create start menu shortcut
set START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs
if not exist "%START_MENU%\\Baresha-Downloader" mkdir "%START_MENU%\\Baresha-Downloader"
echo @echo off > "%START_MENU%\\Baresha-Downloader\\Baresha-Downloader.bat"
echo start "" "%INSTALL_DIR%\\Baresha-Downloader.exe" >> "%START_MENU%\\Baresha-Downloader\\Baresha-Downloader.bat"

echo Installation completed!
echo The application has been installed to: %INSTALL_DIR%
echo Desktop shortcut created.
echo Start menu shortcut created.
pause
'''
        with open('install.bat', 'w') as f:
            f.write(installer_content)
        print("Created Windows installer script: install.bat")
        
    elif platform_name == "macos":
        # macOS installer
        installer_content = '''#!/bin/bash
echo "Baresha Downloader - Installer"
echo "=============================="

# Create installation directory
INSTALL_DIR="/Applications/Baresha-Downloader.app"
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing existing installation..."
    rm -rf "$INSTALL_DIR"
fi

# Copy application
cp -R "dist/Baresha-Downloader.app" "/Applications/"

# Create desktop shortcut
DESKTOP="$HOME/Desktop"
if [ -d "$DESKTOP" ]; then
    ln -sf "/Applications/Baresha-Downloader.app" "$DESKTOP/"
fi

echo "Installation completed!"
echo "The application has been installed to: $INSTALL_DIR"
echo "Desktop shortcut created."
echo ""
echo "You can now launch Baresha Downloader from Applications or Desktop."
'''
        with open('install.sh', 'w') as f:
            f.write(installer_content)
        # Make executable
        os.chmod('install.sh', 0o755)
        print("Created macOS installer script: install.sh")
        
    elif platform_name == "linux":
        # Linux installer
        installer_content = '''#!/bin/bash
echo "Baresha Downloader - Installer"
echo "=============================="

# Create installation directory
INSTALL_DIR="/usr/local/bin"
if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR"
fi

# Copy executable
sudo cp "dist/Baresha-Downloader" "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/Baresha-Downloader"

# Create desktop entry
DESKTOP_ENTRY="$HOME/.local/share/applications/baresha-downloader.desktop"
mkdir -p "$(dirname "$DESKTOP_ENTRY")"

cat > "$DESKTOP_ENTRY" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Baresha Downloader
Comment=YouTube Video Downloader
Exec=$INSTALL_DIR/Baresha-Downloader
Icon=$(pwd)/baresha-logo.jpg
Terminal=false
Categories=Network;Video;
EOF

# Create desktop shortcut
DESKTOP="$HOME/Desktop"
if [ -d "$DESKTOP" ]; then
    cp "$DESKTOP_ENTRY" "$DESKTOP/"
    chmod +x "$DESKTOP/baresha-downloader.desktop"
fi

echo "Installation completed!"
echo "The application has been installed to: $INSTALL_DIR"
echo "Desktop shortcut created."
echo "Application menu entry created."
'''
        with open('install.sh', 'w') as f:
            f.write(installer_content)
        # Make executable
        os.chmod('install.sh', 0o755)
        print("Created Linux installer script: install.sh")

def create_build_script(platform_name):
    """Create a platform-specific build script."""
    
    if platform_name == "windows":
        build_script = '''@echo off
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
'''
        with open('build.bat', 'w') as f:
            f.write(build_script)
        print("Created Windows build script: build.bat")
        
    else:
        # Unix-like systems (macOS/Linux)
        build_script = f'''#!/bin/bash
echo "Baresha Downloader - Building Executable"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

# Install required dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Run the build script
echo "Building executable..."
python3 build_cross_platform.py

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo ""
echo "Build completed successfully!"
echo ""
echo "Files created:"
echo "- dist/Baresha-Downloader (The executable)"
echo "- install.sh (Installation script)"
echo ""
echo "To install the application, run: ./install.sh"
echo ""
'''
        with open('build.sh', 'w') as f:
            f.write(build_script)
        # Make executable
        os.chmod('build.sh', 0o755)
        print("Created Unix build script: build.sh")

def main():
    """Main build function."""
    platform_name, extension = get_platform_info()
    
    print(f"Baresha Downloader - Cross-Platform Executable Builder")
    print(f"Platform: {platform_name}")
    print("=" * 50)
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("Failed to install PyInstaller. Exiting.")
        return 1
    
    # Build executable
    if not build_executable(platform_name, extension):
        print("Failed to build executable. Exiting.")
        return 1
    
    # Create installer scripts
    create_installer_scripts(platform_name, extension)
    
    # Create build script
    create_build_script(platform_name)
    
    print(f"\nBuild completed successfully for {platform_name}!")
    print(f"Executable location: dist/Baresha-Downloader{'.exe' if platform_name == 'windows' else ''}")
    
    if platform_name == "windows":
        print("Installer script: install.bat")
        print("\nTo install the application, run: install.bat")
    else:
        print("Installer script: install.sh")
        print("\nTo install the application, run: ./install.sh")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 