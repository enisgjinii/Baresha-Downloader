#!/usr/bin/env python3
"""
YouTube Video Downloader
A comprehensive tool for downloading YouTube videos with both CLI and GUI interfaces.
Enhanced with FFmpeg-only operation, quality presets, and advanced features.

Features:
- Download videos in various formats and qualities
- Download audio only as MP3, M4A, or AAC
- Preview videos before downloading
- Download history and settings persistence
- System theme detection and dark/light mode support
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp
import requests
from PIL import Image, ImageTk
import urllib.request
from urllib.parse import urlparse
import re
import subprocess
from pathlib import Path
import json
import datetime
from collections import defaultdict
import time
import pystray
from pystray import MenuItem as item

# Import Sun Valley theme
try:
    import sv_ttk
    SUN_VALLEY_AVAILABLE = True
except ImportError:
    SUN_VALLEY_AVAILABLE = False
    print("Warning: Sun Valley theme not available. Using default theme.")

# Import darkdetect for system theme detection
try:
    import darkdetect
    DARKDETECT_AVAILABLE = True
except ImportError:
    DARKDETECT_AVAILABLE = False

# Try to import plyer for notifications
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

# Try to import pystray for system tray
try:
    import pystray
    from pystray import MenuItem as item
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

# Add a simple tooltip helper class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class YouTubeDownloader:
    def __init__(self):
        self.download_path = os.path.expanduser("~/Downloads")
        self.current_download = None
        self.download_thread = None
        self.ffmpeg_path = self.find_ffmpeg()
        self.download_history = self.load_download_history()
        self.settings = self.load_settings()
        
        # Quality presets
        self.quality_presets = {
            "4K Ultra HD": "2160p",
            "2K QHD": "1440p", 
            "1080p Full HD": "1080p",
            "720p HD": "720p",
            "480p SD": "480p",
            "360p": "360p",
            "Best Quality": "best"
        }
        
        # Format presets
        self.format_presets = {
            "MP4 Video": "mp4",
            "MP3 Audio": "mp3",
            "WebM Video": "webm",
            "M4A Audio": "m4a",
            "AAC Audio": "aac",
            "Best Format": "best"
        }
        # Download speed limit (bytes/sec), 0 means unlimited
        self.speed_limit = self.settings.get('speed_limit', 0)
        
    def find_ffmpeg(self):
        """Find FFmpeg installation."""
        # Check if FFmpeg is in PATH
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return 'ffmpeg'
        except:
            pass
        
        # Check if FFmpeg is in project directory
        project_dir = Path(__file__).parent
        ffmpeg_dir = project_dir / "ffmpeg"
        ffmpeg_exe = ffmpeg_dir / "ffmpeg.exe"
        
        if ffmpeg_exe.exists():
            return str(ffmpeg_exe)
        
        return None
        
    def load_download_history(self):
        """Load download history from file."""
        history_file = Path(__file__).parent / "download_history.json"
        try:
            if history_file.exists():
                with open(history_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
        
    def save_download_history(self):
        """Save download history to file."""
        history_file = Path(__file__).parent / "download_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump(self.download_history, f, indent=2)
        except:
            pass
        
    def add_to_history(self, url, title, quality, format_type, status="completed"):
        """Add download to history."""
        entry = {
            "url": url,
            "title": title,
            "quality": quality,
            "format": format_type,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.download_history.append(entry)
        self.save_download_history()
        
    def get_video_info(self, url):
        """Extract video information from YouTube URL."""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            # Add FFmpeg path if available
            if self.ffmpeg_path:
                ydl_opts['ffmpeg_location'] = self.ffmpeg_path
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'formats': info.get('formats', []),
                    'webpage_url': info.get('webpage_url', url),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'upload_date': info.get('upload_date', ''),
                    'description': info.get('description', '')[:200] + "..." if info.get('description', '') else ""
                }
        except Exception as e:
            raise Exception(f"Error extracting video info: {str(e)}")
    
    def download_video(self, url, output_path, quality='best', format_type='mp4', progress_callback=None):
        """Download video with specified quality and format. Supports resume."""
        try:
            # Configure format based on type
            if format_type == 'mp3':
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_callback] if progress_callback else [],
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            elif format_type == 'm4a':
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_callback] if progress_callback else [],
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                        'preferredquality': '192',
                    }],
                }
            elif format_type == 'aac':
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_callback] if progress_callback else [],
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'aac',
                        'preferredquality': '192',
                    }],
                }
            else:
                # Video formats - use proper quality selection
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_callback] if progress_callback else [],
                }
                
                if quality == '2160p':
                    ydl_opts['format'] = 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160]/best'
                elif quality == '1440p':
                    ydl_opts['format'] = 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]/best'
                elif quality == '1080p':
                    ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]/best'
                elif quality == '720p':
                    ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best'
                elif quality == '480p':
                    ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/best'
                elif quality == '360p':
                    ydl_opts['format'] = 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]/best'
                else:
                    ydl_opts['format'] = 'best'
            # Add speed limit if set
            if self.speed_limit and self.speed_limit > 0:
                ydl_opts['ratelimit'] = self.speed_limit
            # Add FFmpeg path if available
            if self.ffmpeg_path:
                ydl_opts['ffmpeg_location'] = self.ffmpeg_path
            # Enable resume
            ydl_opts['continuedl'] = True
            ydl_opts['noprogress'] = False
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")
    
    def get_available_formats(self, url):
        """Get available video formats with detailed information."""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            # Add FFmpeg path if available
            if self.ffmpeg_path:
                ydl_opts['ffmpeg_location'] = self.ffmpeg_path
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)
                formats = []
                
                for f in info.get('formats', []):
                    if f.get('height') and f.get('ext'):
                        format_info = {
                            'format_id': f.get('format_id', ''),
                            'height': f.get('height', 0),
                            'width': f.get('width', 0),
                            'ext': f.get('ext', ''),
                            'filesize': f.get('filesize', 0),
                            'vcodec': f.get('vcodec', 'none'),
                            'acodec': f.get('acodec', 'none'),
                            'fps': f.get('fps', 0),
                            'description': f"{f.get('height', 0)}p ({f.get('width', 0)}x{f.get('height', 0)}) {f.get('ext', '')} - {f.get('vcodec', 'none')}"
                        }
                        formats.append(format_info)
                
                return sorted(formats, key=lambda x: x['height'], reverse=True)
                
        except Exception as e:
            raise Exception(f"Error getting formats: {str(e)}")

    def load_settings(self):
        settings_file = Path(__file__).parent / "settings.json"
        default_settings = {
            "theme": "system",
            "download_path": self.download_path,
            "auto_play": False,
            "default_quality": "Best Quality",
            "default_format": "MP4 Video",
            "clipboard_monitoring": True,
            "speed_limit": 0,
            "language": "en" # Add default language setting
        }
        try:
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    default_settings.update(loaded_settings)
        except:
            pass
        return default_settings

    def save_settings(self):
        settings_file = Path(__file__).parent / "settings.json"
        try:
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass

APP_VERSION = '1.0.0'
UPDATE_CHECK_URL = 'https://example.com/baresha-downloader-version.txt'  # Placeholder

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.downloader = YouTubeDownloader()
        self.language = self.downloader.settings.get('language', 'en')
        self.lang = LANGUAGES[self.language]
        self.root.title(self.lang['app_title'])
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        # Set app icon (window and taskbar)
        try:
            logo_path = str(Path(__file__).parent / 'baresha-logo.jpg')
            self.root.iconphoto(True, tk.PhotoImage(file=logo_path))
        except Exception:
            pass
        self.video_info = None
        self.download_thread = None
        self.current_theme = self.downloader.settings.get('theme', 'system')
        self.clipboard_monitoring = self.downloader.settings.get('clipboard_monitoring', True)
        self.last_clipboard_url = None
        self.setup_theme()
        self.setup_ui()
        self.check_for_updates()
        if self.clipboard_monitoring:
            self.start_clipboard_monitor()
        self.setup_system_tray()
        
    def setup_theme(self):
        """Setup Sun Valley theme."""
        if SUN_VALLEY_AVAILABLE:
            if self.current_theme == "system" and DARKDETECT_AVAILABLE:
                theme = "dark" if darkdetect.isDark() else "light"
            elif self.current_theme == "dark":
                theme = "dark"
            elif self.current_theme == "light":
                theme = "light"
            else:
                theme = "dark"
            sv_ttk.set_theme(theme)
            
            # Configure custom colors for better contrast
            style = ttk.Style()
            style.configure("Title.TLabel", 
                          font=("Segoe UI", 18, "bold"),
                          foreground="#ffffff")
            
            style.configure("Heading.TLabel", 
                          font=("Segoe UI", 11, "bold"),
                          foreground="#ffffff")
            
            style.configure("Info.TLabel", 
                          font=("Segoe UI", 9),
                          foreground="#e0e0e0")
            
            style.configure("Status.TLabel",
                          font=("Segoe UI", 9),
                          foreground="#00ff00")
            
            style.configure("Warning.TLabel",
                          font=("Segoe UI", 9),
                          foreground="#ffaa00")
            
            # Configure custom button styles
            style.configure("Primary.TButton",
                          font=("Segoe UI", 10, "bold"))
            
            style.configure("Secondary.TButton",
                          font=("Segoe UI", 9))
            
            style.configure("Success.TButton",
                          font=("Segoe UI", 9),
                          background="#28a745")
            
            style.configure("Warning.TButton",
                          font=("Segoe UI", 9),
                          background="#ffc107")
        else:
            # Fallback to basic dark theme
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configure dark theme colors
            style.configure(".",
                background="#2b2b2b",
                foreground="#ffffff",
                fieldbackground="#3b3b3b",
                troughcolor="#404040",
                selectbackground="#0078d4",
                selectforeground="#ffffff"
            )
            
            # Configure frames
            style.configure("TFrame", background="#2b2b2b")
            style.configure("TLabelframe", 
                background="#2b2b2b", 
                bordercolor="#404040",
                lightcolor="#404040",
                darkcolor="#404040"
            )
            style.configure("TLabelframe.Label", 
                background="#2b2b2b", 
                foreground="#ffffff",
                font=("Segoe UI", 10, "bold")
            )
            
            # Configure buttons
            style.configure("TButton",
                background="#0078d4",
                foreground="#ffffff",
                bordercolor="#0078d4",
                lightcolor="#0078d4",
                darkcolor="#0078d4",
                focuscolor="#0078d4",
                font=("Segoe UI", 9)
            )
            style.map("TButton",
                background=[("active", "#106ebe"), ("pressed", "#005a9e")],
                foreground=[("active", "#ffffff"), ("pressed", "#ffffff")]
            )
            
            # Configure entry
            style.configure("TEntry",
                fieldbackground="#3b3b3b",
                bordercolor="#404040",
                lightcolor="#404040",
                darkcolor="#404040",
                focuscolor="#0078d4",
                font=("Segoe UI", 9)
            )
            
            # Configure combobox
            style.configure("TCombobox",
                fieldbackground="#3b3b3b",
                background="#3b3b3b",
                bordercolor="#404040",
                lightcolor="#404040",
                darkcolor="#404040",
                focuscolor="#0078d4",
                font=("Segoe UI", 9)
            )
            
            # Configure progress bar
            style.configure("Horizontal.TProgressbar",
                background="#0078d4",
                bordercolor="#0078d4",
                lightcolor="#0078d4",
                darkcolor="#0078d4",
                troughcolor="#404040"
            )
            
            # Configure labels
            style.configure("TLabel",
                background="#2b2b2b",
                foreground="#ffffff",
                font=("Segoe UI", 9)
            )
            
            # Set window background
            self.root.configure(bg="#2b2b2b")
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Status bar at bottom
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(5, 10))
        
        # Status indicators
        self.status_label = ttk.Label(self.status_bar, text="Ready", style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        self.status_label.pack(side=tk.LEFT)
        
        self.download_count_label = ttk.Label(self.status_bar, text="Downloads: 0", style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        self.download_count_label.pack(side=tk.RIGHT)
        
        # Main download tab
        self.setup_download_tab()
        
        # History tab
        self.setup_history_tab()
        
        # Settings tab
        self.setup_settings_tab()
        
        # Update status
        self.update_status()
        
        # Bind window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Add keyboard shortcuts
        self.root.bind('<Control-f>', lambda e: self.focus_search())
        self.root.bind('<Control-d>', lambda e: self.start_download_batch())
        self.root.bind('<Control-p>', lambda e: self.pause_download())
        self.root.bind('<Control-r>', lambda e: self.resume_download())
        self.root.bind('<Control-c>', lambda e: self.cancel_download())
        self.root.bind('<Control-l>', lambda e: self.clear_form())
        self.root.bind('<F5>', lambda e: self.refresh_history())
        
    def setup_download_tab(self):
        """Setup the main download tab."""
        download_frame = ttk.Frame(self.notebook)
        self.notebook.add(download_frame, text=self.lang['download_tab'])
        
        # Configure download frame to expand
        download_frame.columnconfigure(0, weight=1)
        download_frame.rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(download_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)  # Make log section expandable
        
        # Welcome message
        welcome_frame = ttk.LabelFrame(main_frame, text="🎉 Welcome to Baresha Downloader", padding="15")
        welcome_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        welcome_text = """Quick Start Guide:
1. Paste YouTube URLs (one per line) or use the search feature
2. Click 'Fetch Video Info' to preview videos
3. Select quality and format
4. Click 'Download Batch' to start downloading
5. Use Pause/Resume/Cancel to control downloads"""
        welcome_label = ttk.Label(welcome_frame, text=welcome_text, style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel", justify=tk.LEFT)
        welcome_label.pack(anchor=tk.W)
        
        # Logo at the top
        try:
            logo_path = str(Path(__file__).parent / 'baresha-logo.jpg')
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((64, 64), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(main_frame, image=self.logo_photo)
            logo_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 20), pady=(0, 20))
        except Exception:
            pass
        
        # Title
        title_label = ttk.Label(main_frame, text=self.lang['app_title'], 
                               style="Title.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        title_label.grid(row=1, column=1, columnspan=2, pady=(0, 20))
        
        # Status indicators with better styling
        status_frame = ttk.LabelFrame(main_frame, text="📊 System Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # FFmpeg status with color coding
        ffmpeg_status = "✅ FFmpeg Available" if self.downloader.ffmpeg_path else "⚠️ FFmpeg Not Found"
        ffmpeg_style = "Status.TLabel" if self.downloader.ffmpeg_path else "Warning.TLabel"
        ffmpeg_label = ttk.Label(status_frame, text=ffmpeg_status, style=ffmpeg_style)
        ffmpeg_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Download count with icon
        download_count = len(self.downloader.download_history)
        count_label = ttk.Label(status_frame, text=f"📥 Downloads: {download_count}", 
                               style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Language indicator
        lang_label = ttk.Label(status_frame, text=f"🌐 Language: {self.language.upper()}", 
                              style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        lang_label.pack(side=tk.LEFT)
        
        # URL input section with better styling
        url_frame = ttk.LabelFrame(main_frame, text="🔗 YouTube URLs", padding="15")
        url_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        url_frame.columnconfigure(0, weight=1)
        
        ttk.Label(url_frame, text=self.lang['url_label'], 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        # Change from Entry to Text widget for multiple URLs
        self.url_text = tk.Text(url_frame, height=4, width=70, font=("Segoe UI", 10))
        self.url_text.pack(fill=tk.X, pady=(0, 10))
        
        # URL count indicator
        def update_url_count(*args):
            urls = [u.strip() for u in self.url_text.get("1.0", tk.END).splitlines() if u.strip()]
            self.url_count_label.config(text=f"URLs: {len(urls)}")
        self.url_count_label = ttk.Label(url_frame, text="URLs: 0", style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        self.url_count_label.pack(anchor=tk.W)
        self.url_text.bind('<KeyRelease>', update_url_count)
        
        # Drag-and-drop support for URLs
        try:
            import tkinterdnd2 as tkdnd
            self.dnd = tkdnd.TkinterDnD.Tk()  # Only needed for initialization
            self.url_text.drop_target_register(tkdnd.DND_TEXT)
            def drop(event):
                url = event.data.strip()
                if url:
                    self.url_text.insert(tk.END, url + "\n")
                    self.log_message(f"URL added via drag-and-drop: {url}")
                    update_url_count()
            self.url_text.dnd_bind('<<Drop>>', drop)
        except ImportError:
            pass  # Drag-and-drop not available if tkinterdnd2 is not installed
        
        # Buttons frame with better organization
        button_frame = ttk.LabelFrame(main_frame, text="🎮 Controls", padding="15")
        button_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # Primary actions
        primary_frame = ttk.Frame(button_frame)
        primary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.fetch_btn = ttk.Button(primary_frame, text=self.lang['fetch_info'], 
                                   command=self.fetch_video_info_batch, 
                                   style="Primary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.fetch_btn.pack(side=tk.LEFT, padx=(0, 15))

        self.download_btn = ttk.Button(primary_frame, text=self.lang['download_batch'], 
                                      command=self.start_download_batch, state=tk.DISABLED,
                                      style="Success.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.download_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Secondary actions
        secondary_frame = ttk.Frame(button_frame)
        secondary_frame.pack(fill=tk.X)
        
        self.browse_btn = ttk.Button(secondary_frame, text=self.lang['browse_folder'], 
                                    command=self.browse_folder,
                                    style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_folder_btn = ttk.Button(secondary_frame, text=self.lang['open_folder'], 
                                    command=self.open_download_folder,
                                    style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.open_folder_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = ttk.Button(secondary_frame, text=self.lang['clear'], 
                                   command=self.clear_form,
                                   style="Warning.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.preview_btn = ttk.Button(secondary_frame, text=self.lang['preview'], 
                                     command=self.preview_video, state=tk.DISABLED,
                                     style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Help button
        self.help_btn = ttk.Button(secondary_frame, text='❓ Help', 
                                   command=self.show_shortcuts_help,
                                   style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.help_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Download control buttons
        control_frame = ttk.Frame(button_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.pause_btn = ttk.Button(control_frame, text='⏸️ Pause', command=self.pause_download, state=tk.DISABLED, style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.resume_btn = ttk.Button(control_frame, text='▶️ Resume', command=self.resume_download, state=tk.DISABLED, style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.resume_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.cancel_btn = ttk.Button(control_frame, text='❌ Cancel', command=self.cancel_download, state=tk.DISABLED, style="Warning.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # YouTube Search Bar with better styling
        search_frame = ttk.LabelFrame(main_frame, text="🔍 YouTube Search", padding="15")
        search_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text='Search:', style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        def do_search():
            query = self.search_var.get().strip()
            if not query:
                return
            self.search_results_list.delete(0, tk.END)
            self.log_message(f"Searching YouTube for: {query}")
            # Placeholder: In production, use YouTube Data API
            # Here, just show 3 fake results for demo
            for i in range(1, 4):
                self.search_results_list.insert(tk.END, f"https://www.youtube.com/watch?v=FAKEID{i} | Example Video {i} ({query})")
        
        search_btn = ttk.Button(search_frame, text='🔍 Search', command=do_search, style="Primary.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        search_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Search results list
        results_frame = ttk.Frame(search_frame)
        results_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        
        self.search_results_list = tk.Listbox(results_frame, height=3, width=80)
        self.search_results_list.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        def add_selected_url():
            sel = self.search_results_list.curselection()
            if sel:
                url = self.search_results_list.get(sel[0]).split('|')[0].strip()
                self.url_text.insert(tk.END, url + '\n')
                self.log_message(f"Added from search: {url}")
                update_url_count()
        
        add_btn = ttk.Button(results_frame, text='➕ Add to Batch', command=add_selected_url, style="Success.TButton" if SUN_VALLEY_AVAILABLE else "TButton")
        add_btn.grid(row=0, column=1)
        
        # Video info section with enhanced styling
        info_frame = ttk.LabelFrame(main_frame, text=self.lang['video_info'], padding="20")
        info_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 30))
        info_frame.columnconfigure(1, weight=1)
        
        # Thumbnail with better styling
        self.thumbnail_label = ttk.Label(info_frame, text="No thumbnail", 
                                        style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel", 
                                        anchor="center")
        self.thumbnail_label.grid(row=0, column=0, rowspan=6, padx=(0, 20))
        
        # Video details with better layout
        details_frame = ttk.Frame(info_frame)
        details_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_frame.columnconfigure(1, weight=1)
        
        # Title with better styling
        ttk.Label(details_frame, text="📺 Title:", 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_label = ttk.Label(details_frame, text=self.lang['no_video_selected'], 
                                    style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel", 
                                    wraplength=400)
        self.title_label.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Duration with icon
        ttk.Label(details_frame, text="⏱️ Duration:", 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.duration_label = ttk.Label(details_frame, text="--", 
                                       style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        self.duration_label.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Uploader with icon
        ttk.Label(details_frame, text="👤 Uploader:", 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.uploader_label = ttk.Label(details_frame, text="--", 
                                       style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        self.uploader_label.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Views with icon
        ttk.Label(details_frame, text="👁️ Views:", 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.views_label = ttk.Label(details_frame, text="--", 
                                    style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        self.views_label.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Quality and format selection with better styling
        quality_frame = ttk.Frame(details_frame)
        quality_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(quality_frame, text="🎯 Quality:", 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(side=tk.LEFT)
        self.quality_var = tk.StringVar(value="Best Quality")
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                         values=list(self.downloader.quality_presets.keys()),
                                         state="readonly", font=("Segoe UI", 9), width=15)
        self.quality_combo.pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(quality_frame, text="📁 Format:", 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="MP4 Video")
        self.format_combo = ttk.Combobox(quality_frame, textvariable=self.format_var, 
                                        values=list(self.downloader.format_presets.keys()),
                                        state="readonly", font=("Segoe UI", 9), width=15)
        self.format_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Available formats info with icon
        self.formats_label = ttk.Label(details_frame, text="", 
                                      style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel",
                                      wraplength=400)
        self.formats_label.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Download progress with enhanced styling
        progress_frame = ttk.LabelFrame(main_frame, text=self.lang['download_progress'], padding="20")
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 30))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar with better styling
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress label with better styling
        self.progress_label = ttk.Label(progress_frame, text=self.lang['ready_to_download'], 
                                       style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        self.progress_label.grid(row=1, column=0, sticky=tk.W)
        
        # Log section with enhanced styling
        log_frame = ttk.LabelFrame(main_frame, text=self.lang['download_log'], padding="20")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure log text colors based on theme
        if SUN_VALLEY_AVAILABLE:
            log_bg = "#1e1e1e"
            log_fg = "#ffffff"
        else:
            log_bg = "#2b2b2b"
            log_fg = "#ffffff"
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD, 
                                                 font=("Consolas", 9), bg=log_bg, fg=log_fg)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add tooltips to main controls
        ToolTip(self.url_text, "Enter one or more YouTube URLs (one per line)")
        ToolTip(self.fetch_btn, "Fetch video information for all URLs")
        ToolTip(self.download_btn, "Download all fetched videos in batch")
        ToolTip(self.browse_btn, "Choose the download folder")
        ToolTip(self.open_folder_btn, "Open the current download folder in Explorer")
        ToolTip(self.clear_btn, "Clear the form and log")
        ToolTip(self.preview_btn, "Preview the first video in your browser")
        ToolTip(self.quality_combo, "Select the desired video quality")
        ToolTip(self.format_combo, "Select the desired output format")
        ToolTip(self.progress_bar, "Shows overall batch download progress")
        ToolTip(self.pause_btn, "Pause the current batch download")
        ToolTip(self.resume_btn, "Resume the paused batch download")
        ToolTip(self.cancel_btn, "Cancel the current batch download")
        
    def setup_history_tab(self):
        """Setup the download history tab."""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text=self.lang['history_tab'])
        
        # Title
        title_label = ttk.Label(history_frame, text=self.lang['download_history'], 
                               style="Title.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        title_label.pack(pady=20)
        
        # Filter/Search bar
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(pady=(0, 10))
        ttk.Label(filter_frame, text='🔎', style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(side=tk.LEFT)
        self.history_search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.history_search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))
        def filter_history(*args):
            self.refresh_history()
        self.history_search_var.trace_add('write', filter_history)
        
        # History list
        self.history_tree = ttk.Treeview(history_frame, columns=(self.lang['title'], self.lang['quality'], self.lang['format'], self.lang['status'], self.lang['date']), 
                                        show="headings", height=15)
        
        # Configure columns
        self.history_tree.heading(self.lang['title'], text=self.lang['title'])
        self.history_tree.heading(self.lang['quality'], text=self.lang['quality'])
        self.history_tree.heading(self.lang['format'], text=self.lang['format'])
        self.history_tree.heading(self.lang['status'], text=self.lang['status'])
        self.history_tree.heading(self.lang['date'], text=self.lang['date'])
        
        self.history_tree.column(self.lang['title'], width=300)
        self.history_tree.column(self.lang['quality'], width=100)
        self.history_tree.column(self.lang['format'], width=100)
        self.history_tree.column(self.lang['status'], width=100)
        self.history_tree.column(self.lang['date'], width=150)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.history_tree.bind('<<TreeviewSelect>>', self.show_history_thumbnail)
        self.thumbnail_popup = None
        
        # Buttons
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text=self.lang['refresh'], command=self.refresh_history,
                  style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang['clear_history'], command=self.clear_history,
                  style="Warning.TButton" if SUN_VALLEY_AVAILABLE else "TButton").pack(side=tk.LEFT, padx=5)
        
        self.refresh_history()
        
    def setup_settings_tab(self):
        """Setup the settings tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text=self.lang['settings_tab'])
        
        # Title
        title_label = ttk.Label(settings_frame, text=self.lang['settings'], 
                               style="Title.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel")
        title_label.pack(pady=20)
        
        # Settings content
        settings_content = ttk.Frame(settings_frame)
        settings_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Download path
        path_frame = ttk.LabelFrame(settings_content, text=self.lang['download_path'], padding="10")
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.path_var = tk.StringVar(value=self.downloader.download_path)
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(path_frame, text=self.lang['browse'], command=self.browse_download_path,
                  style="Secondary.TButton" if SUN_VALLEY_AVAILABLE else "TButton").pack(side=tk.LEFT)
        
        # FFmpeg settings
        ffmpeg_frame = ttk.LabelFrame(settings_content, text=self.lang['ffmpeg_settings'], padding="10")
        ffmpeg_frame.pack(fill=tk.X, pady=(0, 10))
        
        ffmpeg_status = "✅ Available" if self.downloader.ffmpeg_path else "❌ Not Found"
        ffmpeg_style = "Status.TLabel" if self.downloader.ffmpeg_path else "Warning.TLabel"
        ttk.Label(ffmpeg_frame, text=f"FFmpeg: {ffmpeg_status}", style=ffmpeg_style).pack(anchor=tk.W)
        
        if not self.downloader.ffmpeg_path:
            ttk.Button(ffmpeg_frame, text=self.lang['install_ffmpeg'], command=self.install_ffmpeg,
                      style="Primary.TButton" if SUN_VALLEY_AVAILABLE else "TButton").pack(pady=(10, 0))
        
        # Theme settings
        theme_frame = ttk.LabelFrame(settings_content, text=self.lang['theme_settings'], padding="10")
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(theme_frame, text=self.lang['theme'], 
                 style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(anchor=tk.W)
        theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, 
                                  values=["dark", "light", "system"], 
                                  state="readonly", font=("Segoe UI", 9), width=15)
        theme_combo.pack(anchor=tk.W, pady=(5, 0))
        def change_theme():
            self.current_theme = theme_var.get()
            self.downloader.settings['theme'] = self.current_theme
            self.downloader.save_settings()
            self.setup_theme()
            messagebox.showinfo(self.lang['theme_settings'], self.lang['apply_theme'] + ": " + self.lang['app_title'])
        ttk.Button(theme_frame, text=self.lang['apply_theme'], command=change_theme,
                  style="Primary.TButton" if SUN_VALLEY_AVAILABLE else "TButton").pack(pady=(10, 0))
        
        # Clipboard monitoring toggle
        clipboard_frame = ttk.LabelFrame(settings_content, text=self.lang['clipboard_monitoring'], padding="10")
        clipboard_frame.pack(fill=tk.X, pady=(0, 10))
        self.clipboard_var = tk.BooleanVar(value=self.clipboard_monitoring)
        clipboard_check = ttk.Checkbutton(clipboard_frame, text=self.lang['clipboard_toggle'], variable=self.clipboard_var)
        clipboard_check.pack(anchor=tk.W)
        def toggle_clipboard():
            self.clipboard_monitoring = self.clipboard_var.get()
            self.downloader.settings['clipboard_monitoring'] = self.clipboard_monitoring
            self.downloader.save_settings()
            if self.clipboard_monitoring:
                self.start_clipboard_monitor()
            self.log_message(f"Clipboard monitoring {'enabled' if self.clipboard_monitoring else 'disabled'}.")
        ttk.Button(clipboard_frame, text=self.lang['apply'], command=toggle_clipboard,
                  style="Primary.TButton" if SUN_VALLEY_AVAILABLE else "TButton").pack(pady=(10, 0))
        
        # Speed limit
        speed_frame = ttk.LabelFrame(settings_content, text=self.lang['download_speed_limit'], padding="10")
        speed_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(speed_frame, text=self.lang['max_speed'], style="Heading.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(anchor=tk.W)
        self.speed_var = tk.DoubleVar(value=self.downloader.settings.get('speed_limit', 0) / 1024 / 1024)
        speed_entry = ttk.Entry(speed_frame, textvariable=self.speed_var, width=10)
        speed_entry.pack(anchor=tk.W, pady=(5, 0))
        def apply_speed():
            mbps = self.speed_var.get()
            self.downloader.settings['speed_limit'] = int(mbps * 1024 * 1024)
            self.downloader.save_settings()
            self.downloader.speed_limit = self.downloader.settings['speed_limit']
            self.log_message(f"Speed limit set to {mbps:.2f} MB/s" if mbps > 0 else "Speed limit removed (unlimited)")
        ttk.Button(speed_frame, text=self.lang['apply'], command=apply_speed,
                  style="Primary.TButton" if SUN_VALLEY_AVAILABLE else "TButton").pack(pady=(10, 0))
        
        # Statistics
        stats_frame = ttk.LabelFrame(settings_content, text=self.lang['statistics'], padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        total_downloads = len(self.downloader.download_history)
        successful_downloads = len([d for d in self.downloader.download_history if d.get('status') == 'completed'])
        
        ttk.Label(stats_frame, text=f"{self.lang['total_downloads']} {total_downloads}", 
                 style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"{self.lang['successful_downloads']} {successful_downloads}", 
                 style="Info.TLabel" if SUN_VALLEY_AVAILABLE else "TLabel").pack(anchor=tk.W)
        
    def refresh_history(self):
        """Refresh the download history."""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history items
        query = getattr(self, 'history_search_var', None)
        filter_text = query.get().lower() if query else ''
        for entry in reversed(self.downloader.download_history[-50:]):  # Show last 50
            if filter_text:
                if filter_text not in entry['title'].lower() and filter_text not in entry['status'].lower() and filter_text not in entry['timestamp']:
                    continue
            date = datetime.datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            self.history_tree.insert("", "end", values=(
                entry['title'][:50] + "..." if len(entry['title']) > 50 else entry['title'],
                entry['quality'],
                entry['format'],
                entry['status'],
                date
            ))
            
    def clear_history(self):
        """Clear download history."""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all download history?"):
            self.downloader.download_history = []
            self.downloader.save_download_history()
            self.refresh_history()
            
    def browse_download_path(self):
        """Browse for download path."""
        folder = filedialog.askdirectory(initialdir=self.downloader.download_path)
        if folder:
            self.downloader.download_path = folder
            self.path_var.set(folder)
            
    def install_ffmpeg(self):
        """Install FFmpeg."""
        try:
            import subprocess
            result = subprocess.run([sys.executable, "install_ffmpeg.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", "FFmpeg installed successfully!")
                # Refresh the settings
                self.downloader.ffmpeg_path = self.downloader.find_ffmpeg()
                self.setup_settings_tab()
            else:
                messagebox.showerror("Error", f"Failed to install FFmpeg: {result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install FFmpeg: {str(e)}")
            
    def clear_form(self):
        """Clear the download form."""
        self.url_text.delete("1.0", tk.END)
        self.title_label.config(text=self.lang['no_video_selected'])
        self.duration_label.config(text="--")
        self.uploader_label.config(text="--")
        self.views_label.config(text="--")
        self.formats_label.config(text="")
        self.thumbnail_label.config(text="No thumbnail", image="")
        self.download_btn.config(state=tk.DISABLED)
        self.preview_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progress_label.config(text=self.lang['ready_to_download'])
        self.log_text.delete(1.0, tk.END)
        
    def fetch_video_info_batch(self):
        """Fetch video information for all provided URLs."""
        urls = [u.strip() for u in self.url_text.get("1.0", tk.END).splitlines() if u.strip()]
        if not urls:
            messagebox.showerror(self.lang['error'], "Please enter at least one YouTube URL")
            return
        
        # Validate URLs
        invalid_urls = []
        for url in urls:
            if not ('youtube.com' in url or 'youtu.be' in url):
                invalid_urls.append(url)
        
        if invalid_urls:
            messagebox.showwarning("Invalid URLs", f"The following URLs may not be valid YouTube links:\n{', '.join(invalid_urls[:3])}")
        
        self.fetch_btn.config(state=tk.DISABLED)
        self.log_message(f"Fetching video information for {len(urls)} URL(s)...")
        self.batch_video_info = []
        
        def fetch_thread():
            errors = 0
            for url in urls:
                try:
                    info = self.downloader.get_video_info(url)
                    self.batch_video_info.append(info)
                except Exception as e:
                    error_msg = str(e)
                    if "Video unavailable" in error_msg:
                        self.log_message(f"Video unavailable: {url}", error=True)
                    elif "Private video" in error_msg:
                        self.log_message(f"Private video: {url}", error=True)
                    elif "Video unavailable" in error_msg:
                        self.log_message(f"Video unavailable: {url}", error=True)
                    else:
                        self.log_message(f"Error fetching info for {url}: {error_msg}", error=True)
                    errors += 1
            
            self.root.after(0, lambda: self.update_video_info_batch(errors))
        
        threading.Thread(target=fetch_thread, daemon=True).start()

    def update_video_info_batch(self, errors=0):
        """Update UI after batch info fetch."""
        if not self.batch_video_info:
            self.download_btn.config(state=tk.DISABLED)
            self.log_message("No valid videos found.")
            return
        self.video_info = self.batch_video_info[0]  # Show first video info as preview
        self.update_video_info()
        self.download_btn.config(state=tk.NORMAL)
        self.log_message(f"Ready to download {len(self.batch_video_info)} video(s). Errors: {errors}")

    def start_download_batch(self):
        """Start batch download process."""
        urls = [u.strip() for u in self.url_text.get("1.0", tk.END).splitlines() if u.strip()]
        if not hasattr(self, 'batch_video_info') or not self.batch_video_info:
            messagebox.showerror("Error", "Please fetch video information first")
            return
        quality = self.downloader.quality_presets.get(self.quality_var.get(), "best")
        format_type = self.downloader.format_presets.get(self.format_var.get(), "mp4")
        self.download_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progress_label.config(text="Starting batch download...")
        self._pause_event = threading.Event()
        self._pause_event.set()
        self._cancel_event = threading.Event()
        self.pause_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        # Add animated progress indicator
        self.progress_animation = 0
        def animate_progress():
            if hasattr(self, '_cancel_event') and not self._cancel_event.is_set():
                self.progress_animation = (self.progress_animation + 1) % 4
                dots = "." * self.progress_animation
                self.progress_label.config(text=f"Starting batch download{dots}")
                self.root.after(500, animate_progress)
        animate_progress()
        def batch_thread():
            total = len(self.batch_video_info)
            for idx, info in enumerate(self.batch_video_info):
                if self._cancel_event.is_set():
                    self.root.after(0, lambda: self.log_message('Batch download canceled.', error=True))
                    break
                while not self._pause_event.is_set():
                    time.sleep(0.2)
                url = info['webpage_url']
                title = info['title']
                # If a partial file exists, log that we are resuming
                outtmpl = os.path.join(self.downloader.download_path, '%s.*' % info['title'])
                partials = list(Path(self.downloader.download_path).glob(f"{info['title']}.*.part"))
                if partials:
                    self.root.after(0, lambda: self.log_message(f"Resuming download: {info['title']}"))
                def progress_hook(d, idx=idx):
                    if d['status'] == 'downloading':
                        if 'total_bytes' in d and d['total_bytes']:
                            progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                            # Batch progress: (current video idx + percent of current) / total
                            batch_progress = ((idx + progress/100) / total) * 100
                            self.root.after(0, lambda: self.progress_var.set(batch_progress))
                        speed = d.get('speed', 0)
                        if speed:
                            speed_mb = speed / 1024 / 1024
                            self.root.after(0, lambda: self.progress_label.config(text=f"Downloading {idx+1}/{total}... {speed_mb:.1f} MB/s"))
                    elif d['status'] == 'finished':
                        self.root.after(0, lambda: self.progress_label.config(text=f"Completed {idx+1}/{total}"))
                        self.root.after(0, lambda: self.progress_var.set(((idx+1)/total)*100))
                try:
                    self.downloader.download_video(url, self.downloader.download_path, quality, format_type, progress_hook)
                    self.root.after(0, lambda: self.log_message(f"Downloaded: {title}"))
                    self.downloader.add_to_history(url, title, quality, format_type)
                    self.root.after(0, lambda: self.notify(self.lang['app_title'], f"{title} - Download completed!"))
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"Failed: {title} ({str(e)})"))
                    self.downloader.add_to_history(url, title, quality, format_type, "failed")
                    self.root.after(0, lambda: self.notify(self.lang['app_title'], f"{title} - Download failed!"))
                self.root.after(0, self.refresh_history)
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.pause_btn.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.resume_btn.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.cancel_btn.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.progress_label.config(text="Batch download complete!"))
        self.download_thread = threading.Thread(target=batch_thread, daemon=True)
        self.download_thread.start()
    
    def update_video_info(self):
        """Update the UI with video information."""
        if not self.video_info:
            return
        
        # Update title
        title = self.video_info['title']
        self.title_label.config(text=title[:60] + "..." if len(title) > 60 else title)
        
        # Update duration
        duration = self.video_info['duration']
        if duration:
            minutes = duration // 60
            seconds = duration % 60
            self.duration_label.config(text=f"{minutes}:{seconds:02d}")
        else:
            self.duration_label.config(text="Unknown")
            
        # Update uploader
        uploader = self.video_info.get('uploader', 'Unknown')
        self.uploader_label.config(text=uploader)
        
        # Update views
        views = self.video_info.get('view_count', 0)
        if views:
            self.views_label.config(text=f"{views:,}")
        else:
            self.views_label.config(text="Unknown")
        
        # Update thumbnail
        thumbnail_url = self.video_info.get('thumbnail', '')
        if thumbnail_url:
            self.load_thumbnail(thumbnail_url)
        
        # Fetch and display available formats
        try:
            formats = self.downloader.get_available_formats(self.video_info['webpage_url'])
            if formats:
                # Show top 5 available formats
                format_info = "Available formats: "
                for i, fmt in enumerate(formats[:5]):
                    if i > 0:
                        format_info += ", "
                    format_info += f"{fmt['height']}p"
                self.formats_label.config(text=format_info)
                self.log_message(f"Found {len(formats)} available formats")
            else:
                self.formats_label.config(text="No format information available")
        except Exception as e:
            self.formats_label.config(text="Could not fetch format information")
            self.log_message(f"Warning: Could not get format information: {str(e)}")
        
        self.download_btn.config(state=tk.NORMAL)
        self.preview_btn.config(state=tk.NORMAL)
        self.log_message("Video information loaded successfully")
    
    def load_thumbnail(self, url):
        """Load and display video thumbnail."""
        try:
            def load_thread():
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        image = Image.open(requests.get(url, stream=True).raw)
                        image = image.resize((160, 120), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        self.root.after(0, lambda: self.thumbnail_label.config(image=photo, text=""))
                        def set_image():
                            self.thumbnail_label.image = photo
                        self.root.after(0, set_image)
                except Exception as e:
                    self.root.after(0, lambda: self.thumbnail_label.config(text="Thumbnail error"))
            
            threading.Thread(target=load_thread, daemon=True).start()
        except Exception as e:
            self.thumbnail_label.config(text="Thumbnail error")
    
    def browse_folder(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(initialdir=self.downloader.download_path)
        if folder:
            self.downloader.download_path = folder
            self.log_message(f"Download folder set to: {folder}")
    
    def open_download_folder(self):
        """Open the current download folder in the system file explorer."""
        folder = self.downloader.download_path
        try:
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
            self.log_message(f"Opened folder: {folder}")
        except Exception as e:
            self.log_message(f"Could not open folder: {str(e)}")
    
    def start_download(self):
        """Start the download process."""
        if not self.video_info:
            messagebox.showerror("Error", "Please fetch video information first")
            return
        
        url = self.video_info['webpage_url']
        quality = self.downloader.quality_presets.get(self.quality_var.get(), "best")
        format_type = self.downloader.format_presets.get(self.format_var.get(), "mp4")
        
        self.download_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progress_label.config(text="Starting download...")
        
        def download_thread():
            try:
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        if 'total_bytes' in d and d['total_bytes']:
                            progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                            self.root.after(0, lambda: self.progress_var.set(progress))
                        
                        speed = d.get('speed', 0)
                        if speed:
                            speed_mb = speed / 1024 / 1024
                            self.root.after(0, lambda: self.progress_label.config(text=f"Downloading... {speed_mb:.1f} MB/s"))
                    
                    elif d['status'] == 'finished':
                        self.root.after(0, lambda: self.progress_label.config(text="Download completed!"))
                        self.root.after(0, lambda: self.progress_var.set(100))
                
                self.downloader.download_video(url, self.downloader.download_path, quality, format_type, progress_hook)
                self.root.after(0, lambda: self.log_message("Download completed successfully!"))
                
                # Add to history
                self.downloader.add_to_history(url, self.video_info['title'], quality, format_type)
                self.root.after(0, self.refresh_history)
                
            except Exception as e:
                self.root.after(0, lambda e=e: self.show_error(f"Download failed: {str(e)}"))
                # Add failed download to history
                self.downloader.add_to_history(url, self.video_info['title'], quality, format_type, "failed")
                self.root.after(0, self.refresh_history)
            finally:
                self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
        
        self.download_thread = threading.Thread(target=download_thread, daemon=True)
        self.download_thread.start()
    
    def preview_video(self):
        if not self.video_info:
            messagebox.showerror("Error", "No video selected")
            return
        url = self.video_info['webpage_url']
        try:
            import webbrowser
            webbrowser.open(url)
            self.log_message(f"Opening video in browser: {url}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open browser: {str(e)}")
    
    def log_message(self, message, error=False):
        """Add a message to the log. If error=True, highlight in red."""
        if error:
            self.log_text.insert(tk.END, f"{message}\n", 'error')
            self.log_text.tag_config('error', foreground='red')
        else:
            self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def show_error(self, message):
        """Show an error message."""
        messagebox.showerror("Error", message)
        self.log_message(f"ERROR: {message}", error=True)

    def notify(self, title, message):
        if PLYER_AVAILABLE:
            notification.notify(title=title, message=message, app_name='Baresha Downloader')
        else:
            messagebox.showinfo(title, message)

    def start_clipboard_monitor(self):
        def poll_clipboard():
            if not self.clipboard_monitoring:
                return
            try:
                clipboard = self.root.clipboard_get()
                url_match = re.search(r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+|https?://youtu\.be/[\w-]+)', clipboard)
                if url_match:
                    url = url_match.group(0)
                    if url != self.last_clipboard_url:
                        self.last_clipboard_url = url
                        # Insert into url_text if not already present
                        current = self.url_text.get("1.0", tk.END)
                        if url not in current:
                            self.url_text.insert("1.0", url + "\n")
                            self.log_message(f"Detected YouTube URL from clipboard: {url}")
            except Exception:
                pass
            self.root.after(1500, poll_clipboard)
        self.root.after(1500, poll_clipboard)

    def pause_download(self):
        if hasattr(self, '_pause_event'):
            self._pause_event.clear()
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.NORMAL)
            self.log_message('Batch download paused.')
    def resume_download(self):
        if hasattr(self, '_pause_event'):
            self._pause_event.set()
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)
            self.log_message('Batch download resumed.')
    def cancel_download(self):
        if hasattr(self, '_cancel_event'):
            self._cancel_event.set()
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.DISABLED)
            self.cancel_btn.config(state=tk.DISABLED)
            self.download_btn.config(state=tk.NORMAL)
            self.log_message('Batch download canceled.', error=True)

    def show_history_thumbnail(self, event):
        sel = self.history_tree.selection()
        if not sel:
            return
        item = self.history_tree.item(sel[0])
        title = item['values'][0]
        # Find the entry in history
        entry = next((e for e in self.downloader.download_history if e['title'].startswith(title.rstrip('...'))), None)
        if not entry:
            return
        # Try to get thumbnail from video info
        try:
            info = self.downloader.get_video_info(entry['url'])
            thumb_url = info.get('thumbnail', '')
            if not thumb_url:
                return
            response = requests.get(thumb_url, timeout=10)
            if response.status_code == 200:
                image = Image.open(requests.get(thumb_url, stream=True).raw)
                image = image.resize((320, 180), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                if self.thumbnail_popup:
                    self.thumbnail_popup.destroy()
                self.thumbnail_popup = tk.Toplevel(self.root)
                self.thumbnail_popup.title('Thumbnail Preview')
                label = tk.Label(self.thumbnail_popup, image=photo)
                label.image = photo
                label.pack()
                self.thumbnail_popup.after(5000, self.thumbnail_popup.destroy)
        except Exception:
            pass

    def check_for_updates(self):
        def check():
            try:
                # Placeholder: always say up to date
                # In production, fetch from UPDATE_CHECK_URL
                latest_version = '1.0.0'
                if latest_version != APP_VERSION:
                    self.notify(self.lang['app_title'], f'New version available: {latest_version}')
                else:
                    self.log_message('You are using the latest version.')
            except Exception:
                self.log_message('Could not check for updates.')
        threading.Thread(target=check, daemon=True).start()

    def update_status(self):
        """Update status bar with current information."""
        total_downloads = len(self.downloader.download_history)
        successful = len([d for d in self.downloader.download_history if d.get('status') == 'completed'])
        self.download_count_label.config(text=f"Downloads: {successful}/{total_downloads}")
        
        if hasattr(self, 'current_download'):
            self.status_label.config(text=f"Downloading: {self.current_download}")
        else:
            self.status_label.config(text="Ready")

    def setup_system_tray(self):
        """Setup system tray icon and menu."""
        if not PYSTRAY_AVAILABLE:
            return
        try:
            logo_path = str(Path(__file__).parent / 'baresha-logo.jpg')
            image = Image.open(logo_path)
            image = image.resize((64, 64), Image.LANCZOS)
            
            menu = pystray.Menu(
                item('Show', self.show_window),
                item('Hide', self.hide_window),
                pystray.Menu.SEPARATOR,
                item('Exit', self.quit_app)
            )
            
            self.icon = pystray.Icon("baresha", image, "Baresha Downloader", menu)
            self.icon.run_detached()
        except Exception:
            pass
    
    def show_window(self, icon=None, item=None):
        """Show the main window."""
        self.root.deiconify()
        self.root.lift()
    
    def hide_window(self, icon=None, item=None):
        """Hide the main window."""
        if PYSTRAY_AVAILABLE:
            self.root.withdraw()
        else:
            # If no system tray, just minimize
            self.root.iconify()
    
    def quit_app(self, icon=None, item=None):
        """Quit the application."""
        if PYSTRAY_AVAILABLE and hasattr(self, 'icon'):
            self.icon.stop()
        self.root.quit()
    
    def on_closing(self):
        """Handle window closing."""
        if PYSTRAY_AVAILABLE:
            self.hide_window()
        else:
            self.root.destroy()

    def focus_search(self):
        """Focus on the search entry."""
        try:
            self.search_var.set("")
            # Find the search entry widget and focus it
            for widget in self.root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Entry) and child.cget('textvariable') == str(self.search_var):
                            child.focus_set()
                            break
        except Exception:
            pass
    
    def show_shortcuts_help(self):
        """Show keyboard shortcuts help."""
        shortcuts = """
Keyboard Shortcuts:
Ctrl+F - Focus search
Ctrl+D - Start download
Ctrl+P - Pause download
Ctrl+R - Resume download
Ctrl+C - Cancel download
Ctrl+L - Clear form
F5 - Refresh history
        """
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)

# Language dictionary for English and Albanian
LANGUAGES = {
    'en': {
        'app_title': 'YouTube Video Downloader Pro',
        'download_tab': 'Download',
        'history_tab': 'History',
        'settings_tab': 'Settings',
        'url_label': 'YouTube URL(s):',
        'fetch_info': '🔍 Fetch Video Info',
        'download_batch': '⬇️ Download Batch',
        'browse_folder': '📁 Browse Folder',
        'open_folder': '🗂️ Open Folder',
        'clear': '🧹 Clear',
        'preview': '▶️ Preview',
        'video_info': 'Video Information',
        'download_progress': 'Download Progress',
        'download_log': 'Download Log',
        'no_video_selected': 'No video selected',
        'ready_to_download': 'Ready to download',
        'error': 'Error',
        'clipboard_monitoring': 'Clipboard Monitoring',
        'clipboard_toggle': 'Auto-detect YouTube URLs from clipboard',
        'apply': 'Apply',
        'download_speed_limit': 'Download Speed Limit',
        'max_speed': 'Max speed (MB/s, 0 = unlimited):',
        'statistics': 'Statistics',
        'total_downloads': 'Total Downloads:',
        'successful_downloads': 'Successful Downloads:',
        'theme_settings': 'Theme Settings',
        'theme': 'Theme:',
        'apply_theme': 'Apply Theme',
        'ffmpeg_settings': 'FFmpeg Settings',
        'install_ffmpeg': 'Install FFmpeg',
        'download_path': 'Download Path',
        'browse': 'Browse',
        'clear_history': 'Clear History',
        'refresh': 'Refresh',
        'download_history': 'Download History',
        'title': 'Title',
        'quality': 'Quality',
        'format': 'Format',
        'status': 'Status',
        'date': 'Date',
        'settings': 'Settings',
        'language': 'Language:',
        'english': 'English',
        'albanian': 'Albanian',
    },
    'sq': {
        'app_title': 'Shkarkuesi i Videove në YouTube Pro',
        'download_tab': 'Shkarko',
        'history_tab': 'Historia',
        'settings_tab': 'Cilësimet',
        'url_label': 'URL-të e YouTube:',
        'fetch_info': '🔍 Merr Info për Videon',
        'download_batch': '⬇️ Shkarko në Grup',
        'browse_folder': '📁 Zgjidh Dosjen',
        'open_folder': '🗂️ Hap Dosjen',
        'clear': '🧹 Pastro',
        'preview': '▶️ Parashiko',
        'video_info': 'Informacioni i Videos',
        'download_progress': 'Progresi i Shkarkimit',
        'download_log': 'Logu i Shkarkimit',
        'no_video_selected': 'Asnjë video e zgjedhur',
        'ready_to_download': 'Gati për shkarkim',
        'error': 'Gabim',
        'clipboard_monitoring': 'Monitorimi i Clipboard-it',
        'clipboard_toggle': 'Zbulo automatikisht URL-të e YouTube nga clipboard',
        'apply': 'Apliko',
        'download_speed_limit': 'Kufiri i Shpejtësisë së Shkarkimit',
        'max_speed': 'Shpejtësia maksimale (MB/s, 0 = pa kufi):',
        'statistics': 'Statistikat',
        'total_downloads': 'Shkarkime Gjithsej:',
        'successful_downloads': 'Shkarkime të Suksesshme:',
        'theme_settings': 'Cilësimet e Temës',
        'theme': 'Tema:',
        'apply_theme': 'Apliko Temën',
        'ffmpeg_settings': 'Cilësimet e FFmpeg',
        'install_ffmpeg': 'Instalo FFmpeg',
        'download_path': 'Rruga e Shkarkimit',
        'browse': 'Zgjidh',
        'clear_history': 'Pastro Historinë',
        'refresh': 'Rifresko',
        'download_history': 'Historia e Shkarkimeve',
        'title': 'Titulli',
        'quality': 'Cilësia',
        'format': 'Formati',
        'status': 'Statusi',
        'date': 'Data',
        'settings': 'Cilësimet',
        'language': 'Gjuha:',
        'english': 'Anglisht',
        'albanian': 'Shqip',
    }
}

def main():
    """Main function to run the application."""
    if len(sys.argv) > 1:
        # CLI mode
        run_cli()
    else:
        # GUI mode
        run_gui()

def run_gui():
    """Run the GUI version of the application."""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

def run_cli():
    """Run the CLI version of the application."""
    if len(sys.argv) < 2:
        print("Usage: python youtube_downloader.py <youtube_url> [output_path] [quality] [format]")
        print("Example: python youtube_downloader.py https://www.youtube.com/watch?v=VIDEO_ID")
        print("Quality options: 4K Ultra HD, 2K QHD, 1080p Full HD, 720p HD, 480p SD, 360p, Best Quality")
        print("Format options: MP4 Video, MP3 Audio, WebM Video, M4A Audio, AAC Audio, Best Format")
        return
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/Downloads")
    quality = sys.argv[3] if len(sys.argv) > 3 else "best"
    format_type = sys.argv[4] if len(sys.argv) > 4 else "mp4"
    
    downloader = YouTubeDownloader()
    
    try:
        print(f"Fetching video information for: {url}")
        video_info = downloader.get_video_info(url)
        print(f"Title: {video_info['title']}")
        print(f"Duration: {video_info['duration']} seconds")
        print(f"Uploader: {video_info.get('uploader', 'Unknown')}")
        
        print(f"\nDownloading to: {output_path}")
        print(f"Quality: {quality}")
        print(f"Format: {format_type}")
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    print(f"\rProgress: {progress:.1f}%", end="", flush=True)
            elif d['status'] == 'finished':
                print("\nDownload completed!")
        
        downloader.download_video(url, output_path, quality, format_type, progress_hook)
        print("Download completed successfully!")
        
        # Add to history
        downloader.add_to_history(url, video_info['title'], quality, format_type)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 