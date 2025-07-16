# Baresha Downloader - Cross-Platform Executable Build Guide

This guide explains how to build the Baresha Downloader application into standalone executables for **Windows**, **macOS**, and **Linux**.

## Supported Platforms

- ✅ **Windows 10/11** (64-bit)
- ✅ **macOS 10.15+** (Intel & Apple Silicon)
- ✅ **Linux** (Ubuntu 18.04+, Debian 10+, CentOS 7+, etc.)

## Prerequisites

### All Platforms
- **Python 3.7 or higher** installed on your system
- **Internet connection** (for downloading dependencies)

### Platform-Specific Requirements

#### Windows
- No additional requirements

#### macOS
- **Xcode Command Line Tools** (for compilation)
  ```bash
  xcode-select --install
  ```

#### Linux
- **Build essentials** (for compilation)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install build-essential
  
  # CentOS/RHEL/Fedora
  sudo yum groupinstall "Development Tools"
  # or for newer versions:
  sudo dnf groupinstall "Development Tools"
  ```

## Quick Build

### Windows
```cmd
build.bat
```

### macOS/Linux
```bash
./build.sh
```

## Manual Build Process

### 1. Install Dependencies

```bash
# Windows
pip install -r requirements.txt
pip install pyinstaller

# macOS/Linux
pip3 install -r requirements.txt
pip3 install pyinstaller
```

### 2. Run the Cross-Platform Build Script

```bash
# Windows
python build_cross_platform.py

# macOS/Linux
python3 build_cross_platform.py
```

## Build Output by Platform

### Windows
- **Executable**: `dist/Baresha-Downloader.exe`
- **Installer**: `install.bat`
- **Size**: ~100-200MB

### macOS
- **Application Bundle**: `dist/Baresha-Downloader.app`
- **Installer**: `install.sh`
- **Size**: ~150-250MB

### Linux
- **Binary**: `dist/Baresha-Downloader`
- **Installer**: `install.sh`
- **Size**: ~80-150MB

## Installation by Platform

### Windows Installation

#### Option 1: System Installation (Recommended)
```cmd
install.bat
```
This will:
- Install to `C:\Program Files\Baresha-Downloader\`
- Create desktop shortcut
- Create start menu shortcut

#### Option 2: Portable Usage
```cmd
dist\Baresha-Downloader.exe
```

### macOS Installation

#### Option 1: System Installation (Recommended)
```bash
./install.sh
```
This will:
- Install to `/Applications/Baresha-Downloader.app`
- Create desktop shortcut
- Make it available in Applications folder

#### Option 2: Portable Usage
```bash
open dist/Baresha-Downloader.app
```

### Linux Installation

#### Option 1: System Installation (Recommended)
```bash
./install.sh
```
This will:
- Install to `/usr/local/bin/Baresha-Downloader`
- Create desktop entry
- Create application menu entry
- Create desktop shortcut

#### Option 2: Portable Usage
```bash
./dist/Baresha-Downloader
```

## Platform-Specific Features

### Windows
- ✅ Full GUI support
- ✅ System tray integration
- ✅ Windows notifications
- ✅ Automatic theme detection
- ✅ File association support

### macOS
- ✅ Native macOS app bundle
- ✅ Dock integration
- ✅ macOS notifications
- ✅ Dark/light mode support
- ✅ Apple Silicon (M1/M2) support

### Linux
- ✅ Native Linux binary
- ✅ Desktop environment integration
- ✅ Linux notifications
- ✅ GTK theme support
- ✅ Multiple distribution support

## Cross-Platform Compatibility

### What Works on All Platforms
- ✅ Video downloading (YouTube, Vimeo, etc.)
- ✅ Audio extraction (MP3, M4A, AAC)
- ✅ Quality selection
- ✅ Download history
- ✅ Batch downloads
- ✅ GUI interface
- ✅ Settings persistence

### Platform-Specific Considerations

#### Windows
- **Antivirus**: Some antivirus software may flag PyInstaller executables
- **DLLs**: May require Visual C++ Redistributable
- **Path handling**: Uses Windows path separators

#### macOS
- **Gatekeeper**: May require "Allow Anyway" for first run
- **Code signing**: Not code-signed by default (can be added)
- **Permissions**: May require accessibility permissions for notifications

#### Linux
- **Dependencies**: May need additional system libraries
- **Desktop environment**: Works with GNOME, KDE, XFCE, etc.
- **Permissions**: May need sudo for system installation

## Troubleshooting by Platform

### Windows Issues

#### "Missing DLL" Error
```cmd
# Install Visual C++ Redistributable
# Download from Microsoft's official website
```

#### "Access Denied" During Installation
```cmd
# Run as administrator
runas /user:administrator "install.bat"
```

#### Antivirus Warnings
- Add executable to antivirus whitelist
- The source code is open source and safe

### macOS Issues

#### "App is Damaged" Error
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine dist/Baresha-Downloader.app
```

#### Gatekeeper Blocking
1. Go to System Preferences > Security & Privacy
2. Click "Allow Anyway" for Baresha-Downloader

#### Missing Dependencies
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

### Linux Issues

#### "Permission Denied" Error
```bash
# Make executable
chmod +x dist/Baresha-Downloader
```

#### Missing Libraries
```bash
# Ubuntu/Debian
sudo apt-get install libglib2.0-0 libgtk-3-0 libcairo2

# CentOS/RHEL
sudo yum install glib2 gtk3 cairo
```

#### Desktop Integration Issues
```bash
# Update desktop database
update-desktop-database ~/.local/share/applications
```

## Performance Comparison

| Platform | First Launch | Subsequent Launches | Memory Usage | File Size |
|----------|-------------|-------------------|--------------|-----------|
| Windows  | 10-30s      | 5-10s             | 50-100MB     | 100-200MB |
| macOS    | 15-40s      | 8-15s             | 60-120MB     | 150-250MB |
| Linux    | 8-25s       | 3-8s              | 40-80MB      | 80-150MB  |

## Distribution

### For End Users
- **Windows**: Share `dist/Baresha-Downloader.exe`
- **macOS**: Share `dist/Baresha-Downloader.app`
- **Linux**: Share `dist/Baresha-Downloader`

### For System Installation
- **Windows**: Share executable + `install.bat`
- **macOS**: Share app bundle + `install.sh`
- **Linux**: Share binary + `install.sh`

### For Developers
Share the entire source code repository with build scripts.

## Advanced Build Options

### Custom Icon
Replace `baresha-logo.jpg` with your own icon file.

### Code Signing (macOS)
```bash
# Sign the application
codesign --force --deep --sign "Developer ID Application: Your Name" dist/Baresha-Downloader.app
```

### UPX Compression
The build process automatically uses UPX compression to reduce file size.

### Debug Build
```bash
# Add --debug flag to PyInstaller
pyinstaller --debug Baresha-Downloader.spec
```

## Security Considerations

- **Self-contained**: No external dependencies required
- **Network access**: Only for video downloads
- **Local storage**: Download history stored locally
- **No telemetry**: No data sent to external servers

## Updates

To update the application:

1. Rebuild using the appropriate build script
2. Replace the old executable/app/binary
3. Run the installer again for system installations

## Support

### Getting Help
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Try running the Python version directly
4. Check console output for error messages

### Platform-Specific Support
- **Windows**: Check Windows Event Viewer for errors
- **macOS**: Check Console.app for system logs
- **Linux**: Check system logs with `journalctl`

---

**Note**: This build system creates platform-specific executables. Each executable will only run on its target platform. For multi-platform distribution, you'll need to build on each target platform or use cross-compilation tools. 