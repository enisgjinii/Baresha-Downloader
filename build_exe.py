#!/usr/bin/env python3
"""
Build script for creating executable from YouTube Video Downloader
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

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

def create_spec_file():
    """Create a PyInstaller spec file for the application."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['youtube_downloader.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('baresha-logo.jpg', '.'),
        ('ffmpeg', 'ffmpeg'),
        ('install_ffmpeg.py', '.'),
    ],
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
    hooksconfig={},
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='baresha-logo.jpg',
)
'''
    
    with open('Baresha-Downloader.spec', 'w') as f:
        f.write(spec_content)
    print("Created PyInstaller spec file: Baresha-Downloader.spec")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Create spec file
    create_spec_file()
    
    # Build the executable
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "Baresha-Downloader.spec"
        ])
        print("Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build executable: {e}")
        return False

def create_installer_script():
    """Create a simple installer script."""
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
    print("Created installer script: install.bat")

def main():
    """Main build function."""
    print("Baresha Downloader - Executable Builder")
    print("=" * 40)
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("Failed to install PyInstaller. Exiting.")
        return 1
    
    # Build executable
    if not build_executable():
        print("Failed to build executable. Exiting.")
        return 1
    
    # Create installer script
    create_installer_script()
    
    print("\nBuild completed successfully!")
    print("Executable location: dist/Baresha-Downloader.exe")
    print("Installer script: install.bat")
    print("\nTo install the application, run: install.bat")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 