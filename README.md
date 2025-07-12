# YouTube Video Downloader

A comprehensive Python application for downloading YouTube videos with both graphical user interface (GUI) and command-line interface (CLI) support, featuring a modern Sun Valley theme and integrated FFmpeg support.

## Features

- **Dual Interface**: Both GUI and CLI modes
- **Modern UI**: Beautiful Sun Valley ttk theme with dark mode
- **Video Information**: Fetch and display video details before downloading
- **Quality Selection**: Choose from available video qualities
- **Progress Tracking**: Real-time download progress with speed indicators
- **Thumbnail Preview**: Display video thumbnails in GUI mode
- **Custom Download Path**: Choose where to save downloaded videos
- **FFmpeg Integration**: Local FFmpeg installation for better format support
- **Error Handling**: Comprehensive error handling and user feedback

## Installation

1. **Clone or download this repository**
2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install FFmpeg locally** (optional but recommended):
   ```bash
   python install_ffmpeg.py
   ```

## Usage

### GUI Mode (Default)
Run the application without arguments to launch the graphical interface:
```bash
python youtube_downloader.py
```

**GUI Features:**
- Modern Sun Valley dark theme
- Enter YouTube URL in the text field
- Click "Fetch Video Info" to get video details
- Select desired quality from the dropdown
- Choose download folder using "Browse Folder"
- Click "Download" to start downloading
- Monitor progress in real-time
- FFmpeg status indicator

### CLI Mode
Run with a YouTube URL as argument:
```bash
python youtube_downloader.py <youtube_url> [output_path] [quality]
```

**Examples:**
```bash
# Download with default settings
python youtube_downloader.py https://www.youtube.com/watch?v=VIDEO_ID

# Download to specific folder
python youtube_downloader.py https://www.youtube.com/watch?v=VIDEO_ID /path/to/folder

# Download with specific quality
python youtube_downloader.py https://www.youtube.com/watch?v=VIDEO_ID /path/to/folder 720p
```

## Requirements

- Python 3.7+
- yt-dlp (for video downloading)
- Pillow (for image processing)
- requests (for HTTP requests)
- sv-ttk (Sun Valley theme)
- ffmpeg-python (for FFmpeg integration)
- tkinter (usually included with Python)

## How It Works

The application uses `yt-dlp` (a fork of youtube-dl) to handle YouTube video downloading. It provides:

1. **Video Information Extraction**: Fetches metadata like title, duration, and available formats
2. **Format Selection**: Allows users to choose from available video qualities
3. **Progress Monitoring**: Real-time download progress with speed indicators
4. **FFmpeg Integration**: Local FFmpeg installation for better format support and conversions
5. **Modern UI**: Sun Valley theme for a beautiful, modern interface

## File Structure

```
Baresha-Downloader/
├── youtube_downloader.py    # Main application file
├── install_ffmpeg.py        # FFmpeg installer script
├── requirements.txt         # Python dependencies
├── run.bat                 # Windows launcher
├── run.sh                  # Linux/macOS launcher
├── run.py                  # Python launcher
├── ffmpeg/                 # Local FFmpeg installation
│   ├── ffmpeg.exe
│   ├── ffplay.exe
│   └── ffprobe.exe
└── README.md              # This documentation
```

## Features

### Sun Valley Theme
- Modern dark theme with beautiful styling
- Consistent with modern UI design principles
- Automatic fallback to dark theme if Sun Valley is not available

### FFmpeg Integration
- Local FFmpeg installation in project directory
- Automatic detection and configuration
- Better format support and video processing
- No system-wide installation required

### Enhanced Download Capabilities
- Support for various video formats
- Audio extraction capabilities
- Better quality selection with FFmpeg
- Improved error handling

## Troubleshooting

### Common Issues

1. **"Module not found" errors**: Make sure to install dependencies with `pip install -r requirements.txt`

2. **Download fails**: 
   - Check your internet connection
   - Verify the YouTube URL is valid and accessible
   - Some videos may be region-restricted or private

3. **GUI doesn't start**: 
   - Ensure tkinter is installed (usually included with Python)
   - On Linux, you might need to install `python3-tk`

4. **FFmpeg not found**: 
   - Run `python install_ffmpeg.py` to install FFmpeg locally
   - The downloader will work without FFmpeg but with limited features

5. **Permission errors**: 
   - Make sure you have write permissions to the download directory
   - Try running as administrator if needed

### Performance Tips

- Use wired internet connection for faster downloads
- Close other bandwidth-heavy applications during download
- Choose lower quality for faster downloads
- FFmpeg installation provides better format support

## Legal Notice

This tool is for personal use only. Please respect YouTube's Terms of Service and only download content you have permission to download. The developers are not responsible for any misuse of this software.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## License

This project is open source and available under the MIT License. 