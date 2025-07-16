# Baresha Downloader - Executable Build Guide

This guide explains how to build the Baresha Downloader application into a standalone executable (.exe) file.

## Prerequisites

1. **Python 3.7 or higher** installed on your system
2. **Windows 10/11** (the build process is optimized for Windows)
3. **Internet connection** (for downloading dependencies)

## Quick Build

The easiest way to build the executable is to run the provided batch file:

```bash
build.bat
```

This will:
1. Check if Python is installed
2. Install all required dependencies
3. Build the executable using PyInstaller
4. Create an installer script

## Manual Build Process

If you prefer to build manually, follow these steps:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Run the Build Script

```bash
python build_exe.py
```

### 3. Alternative: Direct PyInstaller Command

```bash
pyinstaller --onefile --windowed --icon=baresha-logo.jpg --name="Baresha-Downloader" youtube_downloader.py
```

## Build Output

After a successful build, you'll find:

- **`dist/Baresha-Downloader.exe`** - The main executable
- **`install.bat`** - Installation script for system-wide installation
- **`Baresha-Downloader.spec`** - PyInstaller specification file

## Installation

### Option 1: Simple Installation
Run the installer script as administrator:
```bash
install.bat
```

This will:
- Install the application to `C:\Program Files\Baresha-Downloader\`
- Create desktop shortcut
- Create start menu shortcut

### Option 2: Portable Usage
Simply run the executable directly:
```bash
dist/Baresha-Downloader.exe
```

## Features of the Executable

The built executable includes:

- **All dependencies bundled** - No need to install Python or any packages
- **FFmpeg integration** - Video processing capabilities included
- **GUI interface** - Full graphical user interface
- **System tray support** - Minimize to system tray
- **Dark/light theme support** - Automatic theme detection
- **Download history** - Persistent download tracking
- **Batch download support** - Download multiple videos at once

## Troubleshooting

### Common Issues

1. **"Missing DLL" errors**
   - Install Microsoft Visual C++ Redistributable
   - Download from Microsoft's official website

2. **"Access denied" during installation**
   - Run `install.bat` as administrator
   - Or use the portable version directly

3. **Large file size**
   - The executable includes all dependencies (~100-200MB)
   - This is normal for Python applications with GUI

4. **Antivirus warnings**
   - Some antivirus software may flag PyInstaller-built executables
   - Add the executable to your antivirus whitelist
   - The source code is open source and safe

### Build Issues

1. **PyInstaller not found**
   ```bash
   pip install pyinstaller
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission errors**
   - Run command prompt as administrator
   - Check antivirus software

## File Structure After Build

```
Baresha-Downloader/
├── dist/
│   └── Baresha-Downloader.exe    # Main executable
├── build/                        # Build artifacts (can be deleted)
├── __pycache__/                  # Python cache (can be deleted)
├── install.bat                   # Installation script
├── build.bat                     # Build script
├── build_exe.py                  # Build automation script
└── Baresha-Downloader.spec       # PyInstaller spec file
```

## Distribution

To distribute your application:

1. **For end users**: Share the `dist/Baresha-Downloader.exe` file
2. **For system installation**: Share both the executable and `install.bat`
3. **For developers**: Share the entire source code repository

## Performance Notes

- **First launch**: May take 10-30 seconds to start (loading bundled libraries)
- **Subsequent launches**: Much faster (5-10 seconds)
- **Memory usage**: ~50-100MB during operation
- **Disk space**: ~200-300MB for the complete installation

## Security Considerations

- The executable is self-contained and doesn't require internet access for basic operation
- All network requests are made through the yt-dlp library
- No data is sent to external servers except for video downloads
- Download history is stored locally in JSON format

## Updates

To update the application:

1. Rebuild the executable using `build.bat`
2. Replace the old executable with the new one
3. Or run the installer again to update the installed version

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Try running the Python version directly to isolate issues
4. Check the console output for error messages

---

**Note**: This executable is built specifically for Windows. For other operating systems, you'll need to modify the build process accordingly. 