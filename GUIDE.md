# 📖 Baresha Downloader User Guide

**Complete guide to using Baresha Downloader Pro**

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Settings & Configuration](#settings--configuration)
5. [Troubleshooting](#troubleshooting)
6. [Tips & Tricks](#tips--tricks)
7. [FAQ](#faq)

---

## 🚀 Getting Started

### First Launch
1. **Install Python** (3.8 or higher)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the app**: `python youtube_downloader.py`

### Initial Setup
- The app will create default settings on first run
- Download folder defaults to your system's Downloads folder
- Language defaults to English (can be changed in Settings)

---

## 📝 Basic Usage

### Step 1: Adding YouTube URLs
There are several ways to add YouTube URLs:

#### Method 1: Direct Input
1. Click in the URL text area
2. Paste one or more YouTube URLs (one per line)
3. Example:
   ```
   https://www.youtube.com/watch?v=VIDEO_ID_1
   https://www.youtube.com/watch?v=VIDEO_ID_2
   https://youtu.be/VIDEO_ID_3
   ```

#### Method 2: Drag & Drop
1. Copy YouTube URLs to clipboard
2. Drag them into the URL text area
3. URLs will be automatically added

#### Method 3: Clipboard Monitoring
1. Enable clipboard monitoring in Settings
2. Copy any YouTube URL to clipboard
3. URL will be automatically detected and added

#### Method 4: YouTube Search
1. Use the search bar to find videos
2. Type your search query
3. Select videos from results
4. Click "Add to Batch"

### Step 2: Fetching Video Information
1. Click **"🔍 Fetch Video Info"** button
2. Wait for the app to retrieve video details
3. Review the information displayed:
   - **Title**: Video title
   - **Duration**: Video length
   - **Uploader**: Channel name
   - **Views**: View count
   - **Thumbnail**: Video preview image

### Step 3: Selecting Quality & Format
Choose your preferred settings:

#### Quality Options:
- **4K Ultra HD** (2160p) - Highest quality
- **2K QHD** (1440p) - Very high quality
- **1080p Full HD** - High quality
- **720p HD** - Standard quality
- **480p SD** - Lower quality
- **360p** - Low quality
- **Best Quality** - Automatic selection

#### Format Options:
- **MP4 Video** - Standard video format
- **MP3 Audio** - Audio only, MP3 format
- **WebM Video** - Web-optimized video
- **M4A Audio** - Audio only, M4A format
- **AAC Audio** - Audio only, AAC format
- **Best Format** - Automatic selection

### Step 4: Downloading
1. Click **"⬇️ Download Batch"** button
2. Monitor progress in the progress bar
3. Check the log for detailed information
4. Use control buttons as needed:
   - **⏸️ Pause**: Temporarily stop download
   - **▶️ Resume**: Continue paused download
   - **❌ Cancel**: Stop download completely

---

## 🔧 Advanced Features

### Batch Downloads
**Download multiple videos simultaneously:**

1. Add multiple URLs to the text area
2. Fetch video information for all
3. Select quality and format
4. Start batch download
5. Monitor overall progress

**Tips:**
- Batch downloads are processed sequentially
- Progress bar shows overall completion
- Each video is downloaded individually
- Failed downloads don't stop the batch

### YouTube Search
**Find videos directly in the app:**

1. Enter search terms in the search bar
2. Click **"🔍 Search"**
3. Browse results in the list
4. Select desired videos
5. Click **"➕ Add to Batch"**

**Note:** Search results are currently placeholder data. In a full implementation, this would connect to YouTube's API.

### Clipboard Monitoring
**Automatically detect YouTube URLs:**

1. Go to **Settings** tab
2. Enable **"Auto-detect YouTube URLs from clipboard"**
3. Click **"Apply"**
4. Copy any YouTube URL to clipboard
5. URL will be automatically added to batch

### System Tray
**Minimize to system tray:**

1. Click the **X** button to minimize to tray
2. Right-click tray icon for options:
   - **Show**: Restore window
   - **Hide**: Minimize to tray
   - **Exit**: Close application

### Download History
**Track and manage past downloads:**

1. Go to **History** tab
2. View all past downloads
3. Use search/filter to find specific downloads
4. Click on entries to see thumbnails
5. Use **"Rifresko"** to update list

### Keyboard Shortcuts
**Power user shortcuts:**

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl+F` | Focus Search | Focus on search bar |
| `Ctrl+D` | Start Download | Begin batch download |
| `Ctrl+P` | Pause | Pause current download |
| `Ctrl+R` | Resume | Resume paused download |
| `Ctrl+C` | Cancel | Cancel current download |
| `Ctrl+L` | Clear | Clear form and log |
| `F5` | Refresh | Refresh download history |

---

## ⚙️ Settings & Configuration

### Language Settings
**Switch between English and Albanian:**

1. Go to **Settings** tab
2. Select language from dropdown
3. Click **"Apply"**
4. App will restart with new language

### Download Settings

#### Download Path
1. Click **"Browse"** next to download path
2. Select your preferred folder
3. Path will be saved automatically

#### Speed Limit
1. Enter maximum speed in MB/s
2. Use **0** for unlimited speed
3. Click **"Apply"** to save

**Recommended speeds:**
- **1-2 MB/s**: Light browsing
- **5-10 MB/s**: Normal usage
- **0**: Unlimited (fastest)

### Theme Settings
**Choose your preferred theme:**

1. Select theme from dropdown:
   - **System**: Follows system theme
   - **Dark**: Always dark theme
   - **Light**: Always light theme
2. Click **"Apply Theme"**

### Clipboard Monitoring
**Enable/disable automatic URL detection:**

1. Check/uncheck the option
2. Click **"Apply"**
3. Changes take effect immediately

---

## 🔧 Troubleshooting

### Common Issues

#### App Won't Start
**Problem:** Application fails to launch

**Solutions:**
1. **Check Python version**: Ensure Python 3.8+ is installed
2. **Install dependencies**: Run `pip install -r requirements.txt`
3. **Check tkinter**: Ensure tkinter is available
4. **Windows**: Install `python-tk` package

#### Download Fails
**Problem:** Videos won't download

**Solutions:**
1. **Check internet connection**
2. **Verify URL format**: Ensure it's a valid YouTube URL
3. **Check video availability**: Some videos may be private/restricted
4. **Try different quality**: Lower quality may work better
5. **Check disk space**: Ensure enough storage space

#### FFmpeg Not Found
**Problem:** FFmpeg-related errors

**Solutions:**
1. **Install FFmpeg**: Run `python install_ffmpeg.py`
2. **Manual installation**: Download FFmpeg from official website
3. **Add to PATH**: Add FFmpeg to system PATH
4. **Continue without FFmpeg**: App works with limited features

#### Slow Downloads
**Problem:** Downloads are very slow

**Solutions:**
1. **Check internet speed**
2. **Reduce quality**: Choose lower video quality
3. **Close other apps**: Free up bandwidth
4. **Check speed limit**: Ensure speed limit isn't too low
5. **Try different time**: Network may be congested

#### GUI Issues
**Problem:** Interface problems

**Solutions:**
1. **Update theme**: Try different theme in settings
2. **Restart app**: Close and reopen application
3. **Check display settings**: Ensure proper resolution
4. **Update graphics drivers**: Update system drivers

### Error Messages

#### "Video unavailable"
- Video may be private or deleted
- Try a different video
- Check if video is region-restricted

#### "Private video"
- Video requires authentication
- Cannot download private videos
- Try public videos only

#### "Network error"
- Check internet connection
- Try again later
- Check firewall settings

#### "Permission denied"
- Check folder permissions
- Run as administrator (Windows)
- Choose different download folder

---

## 💡 Tips & Tricks

### Performance Optimization

#### Faster Downloads
1. **Use wired connection** instead of WiFi
2. **Close bandwidth-heavy apps** (streaming, gaming)
3. **Choose appropriate quality** (720p is often sufficient)
4. **Download during off-peak hours**

#### Better Quality
1. **Install FFmpeg** for enhanced processing
2. **Choose higher quality** when available
3. **Use MP4 format** for best compatibility
4. **Check video source quality** before downloading

#### Batch Download Tips
1. **Group similar videos** for consistent quality
2. **Use pause/resume** for long batches
3. **Monitor disk space** for large downloads
4. **Check download folder** regularly

### Keyboard Shortcuts Mastery
1. **Learn essential shortcuts**: Ctrl+D, Ctrl+P, Ctrl+R
2. **Use F5** to refresh history quickly
3. **Ctrl+L** to clear form when starting new batch
4. **Ctrl+F** to focus search for quick access

### Organization Tips
1. **Use descriptive folder names** for downloads
2. **Create subfolders** by category or channel
3. **Regularly clean download history**
4. **Backup important downloads**

---

## ❓ FAQ

### General Questions

**Q: Is this app legal to use?**
A: Yes, for personal use. Respect YouTube's Terms of Service and only download content you have permission to access.

**Q: Can I download private videos?**
A: No, only public videos can be downloaded.

**Q: What's the maximum quality I can download?**
A: Up to 4K Ultra HD (2160p), depending on the video's original quality.

**Q: Can I download playlists?**
A: Currently, individual videos only. Playlist support may be added in future versions.

### Technical Questions

**Q: Why do some downloads fail?**
A: Common reasons include:
- Video is private or deleted
- Region restrictions
- Network issues
- Insufficient disk space

**Q: How do I update the app?**
A: The app checks for updates automatically. Manual updates require downloading the latest version.

**Q: Can I use this on mobile?**
A: No, this is a desktop application. Mobile versions may be developed in the future.

**Q: What formats are supported?**
A: MP4, MP3, WebM, M4A, and AAC formats are supported.

### Feature Questions

**Q: How does batch download work?**
A: Videos are downloaded one at a time in sequence. You can pause, resume, or cancel the entire batch.

**Q: Can I schedule downloads?**
A: Not currently, but this feature may be added in future versions.

**Q: How do I change the download folder?**
A: Go to Settings → Download Path → Browse to select a new folder.

**Q: Can I download audio only?**
A: Yes, select MP3, M4A, or AAC format to download audio only.

### Troubleshooting Questions

**Q: The app is slow, what can I do?**
A: Try reducing video quality, closing other apps, or checking your internet connection.

**Q: Downloads keep failing, help!**
A: Check your internet connection, try different videos, or restart the app.

**Q: Can't find FFmpeg, what should I do?**
A: Run `python install_ffmpeg.py` or download FFmpeg manually from the official website.

**Q: The interface looks wrong, how to fix?**
A: Try changing the theme in Settings, or restart the application.

---

## 📞 Support

### Getting Help
- **Check this guide** for common solutions
- **Review troubleshooting section** for specific issues
- **Check GitHub Issues** for known problems
- **Contact support** for complex issues

### Reporting Issues
When reporting issues, please include:
1. **Operating system** and version
2. **Python version**
3. **Error message** (if any)
4. **Steps to reproduce** the issue
5. **YouTube URL** (if relevant)

### Feature Requests
We welcome feature requests! Please:
1. **Check existing issues** first
2. **Describe the feature** clearly
3. **Explain the use case**
4. **Provide examples** if possible

---

**Happy downloading! 🎬**

*For the latest updates and support, visit our GitHub repository.* 