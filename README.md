# 🎬 Baresha Downloader Pro

**A powerful, feature-rich YouTube video downloader with bilingual support and modern UI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/baresha-downloader)

## 🌟 Features

### 🎯 Core Features
- **Batch Download**: Download multiple videos simultaneously
- **Multiple Formats**: MP4, MP3, WebM, M4A, AAC support
- **Quality Selection**: From 360p to 4K Ultra HD
- **Download Resume**: Automatically resume interrupted downloads
- **Speed Limiting**: Control download speed to manage bandwidth

### 🌍 Bilingual Support
- **English & Albanian** interface
- **Language switching** in settings
- **Localized error messages** and tooltips

### 🎨 Modern UI/UX
- **Dark/Light theme** with system detection
- **Sun Valley theme** support for modern look
- **Animated progress indicators**
- **System tray integration**
- **Keyboard shortcuts** for power users
- **Drag & drop** URL support

### 🔍 Advanced Features
- **YouTube Search**: Find videos directly in the app
- **Clipboard Monitoring**: Auto-detect YouTube URLs
- **Download History**: Track and filter past downloads
- **Thumbnail Previews**: See video thumbnails in history
- **Download Notifications**: Desktop notifications on completion
- **Queue Management**: Pause, resume, cancel downloads

### 🛠️ Technical Features
- **FFmpeg Integration**: High-quality audio/video processing
- **Auto-update Checker**: Stay updated with latest version
- **Error Handling**: User-friendly error messages
- **Cross-platform**: Windows, macOS, Linux support

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (optional, for enhanced features)

### Quick Install
```bash
# Clone the repository
git clone https://github.com/your-username/baresha-downloader.git
cd baresha-downloader

# Install dependencies
pip install -r requirements.txt

# Run the application
python youtube_downloader.py
```

### Optional Dependencies
For enhanced features, install additional packages:
```bash
pip install pystray plyer
```

## 🚀 Usage

### Basic Usage
1. **Launch the app**: Run `python youtube_downloader.py`
2. **Add URLs**: Paste YouTube URLs (one per line)
3. **Fetch Info**: Click "Fetch Video Info" to preview
4. **Select Quality**: Choose your preferred quality and format
5. **Download**: Click "Download Batch" to start

### Advanced Features

#### Batch Downloads
- Add multiple URLs to download several videos at once
- Monitor progress with the enhanced progress bar
- Use Pause/Resume/Cancel controls

#### YouTube Search
- Use the search bar to find videos
- Select from search results to add to batch
- Search results are added automatically

#### Clipboard Monitoring
- Enable in Settings → Clipboard Monitoring
- Automatically detects YouTube URLs copied to clipboard
- Adds URLs to the batch automatically

#### System Tray
- Minimize to system tray for background operation
- Right-click tray icon for quick actions
- Desktop notifications for download completion

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Focus search |
| `Ctrl+D` | Start download |
| `Ctrl+P` | Pause download |
| `Ctrl+R` | Resume download |
| `Ctrl+C` | Cancel download |
| `Ctrl+L` | Clear form |
| `F5` | Refresh history |

## 🎛️ Settings

### Language Settings
- Switch between English and Albanian
- Changes apply immediately
- All UI elements are localized

### Download Settings
- **Download Path**: Set default download folder
- **Speed Limit**: Control maximum download speed
- **Default Quality**: Set preferred video quality
- **Default Format**: Set preferred output format

### Theme Settings
- **System**: Follows system theme
- **Dark**: Always use dark theme
- **Light**: Always use light theme

### Clipboard Monitoring
- Enable/disable automatic URL detection
- Works with YouTube URLs copied to clipboard
- Adds URLs automatically to batch

## 📊 Features Overview

| Feature | Status | Description |
|---------|--------|-------------|
| Batch Download | ✅ | Download multiple videos |
| Quality Selection | ✅ | 360p to 4K support |
| Format Support | ✅ | MP4, MP3, WebM, M4A, AAC |
| Bilingual UI | ✅ | English & Albanian |
| Dark Theme | ✅ | Modern dark interface |
| System Tray | ✅ | Background operation |
| Keyboard Shortcuts | ✅ | Power user features |
| Download Resume | ✅ | Resume interrupted downloads |
| Speed Limiting | ✅ | Bandwidth control |
| YouTube Search | ✅ | Find videos in app |
| Clipboard Monitor | ✅ | Auto-detect URLs |
| Download History | ✅ | Track past downloads |
| Thumbnail Preview | ✅ | See video thumbnails |
| Notifications | ✅ | Desktop notifications |
| Queue Management | ✅ | Pause/Resume/Cancel |
| Error Handling | ✅ | User-friendly errors |
| Auto-updates | ✅ | Version checking |

## 🛠️ Technical Details

### Architecture
- **GUI Framework**: Tkinter with Sun Valley theme
- **Download Engine**: yt-dlp for YouTube downloads
- **Image Processing**: Pillow for thumbnails
- **System Integration**: pystray for system tray
- **Notifications**: plyer for desktop notifications

### File Structure
```
baresha-downloader/
├── youtube_downloader.py    # Main application
├── requirements.txt         # Python dependencies
├── baresha-logo.jpg        # Application logo
├── settings.json           # User settings
├── download_history.json   # Download history
├── install_ffmpeg.py      # FFmpeg installer
├── run.bat                # Windows launcher
├── run.sh                 # Linux/macOS launcher
└── README.md              # This file
```

### Dependencies
- **yt-dlp**: YouTube download engine
- **Pillow**: Image processing
- **requests**: HTTP requests
- **sv-ttk**: Modern UI theme
- **darkdetect**: System theme detection
- **pystray**: System tray integration (optional)
- **plyer**: Desktop notifications (optional)

## 🎨 Screenshots

*[Screenshots will be added here showing the main interface, settings, and history tabs]*

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-username/baresha-downloader.git
cd baresha-downloader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python youtube_downloader.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **yt-dlp** team for the excellent YouTube download engine
- **Sun Valley** theme creators for the modern UI
- **Pillow** team for image processing capabilities
- **Tkinter** community for the GUI framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/baresha-downloader/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/baresha-downloader/discussions)
- **Email**: support@baresha-downloader.com

## 🔄 Changelog

### Version 1.0.0
- ✨ Initial release with bilingual support
- ✨ Modern UI with Sun Valley theme
- ✨ Batch download capabilities
- ✨ System tray integration
- ✨ Keyboard shortcuts
- ✨ Download history and filtering
- ✨ YouTube search functionality
- ✨ Clipboard monitoring
- ✨ Download notifications
- ✨ Thumbnail previews
- ✨ Queue management (pause/resume/cancel)
- ✨ Auto-update checker
- ✨ Download resume support

---

**Made with ❤️ by the Baresha Team**

*Download YouTube videos with style and ease!* 