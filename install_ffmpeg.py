#!/usr/bin/env python3
"""
FFmpeg installer for YouTube Downloader project
Downloads and installs FFmpeg locally in the project directory
"""

import os
import sys
import zipfile
import requests
import subprocess
from pathlib import Path

def download_file(url, filename):
    """Download a file with progress indicator."""
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end="", flush=True)
    print()

def install_ffmpeg():
    """Download and install FFmpeg for Windows."""
    # Create ffmpeg directory in project
    project_dir = Path(__file__).parent
    ffmpeg_dir = project_dir / "ffmpeg"
    ffmpeg_dir.mkdir(exist_ok=True)
    
    # FFmpeg download URL for Windows
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_filename = "ffmpeg.zip"
    
    try:
        # Download FFmpeg
        print("Downloading FFmpeg...")
        download_file(ffmpeg_url, zip_filename)
        
        # Extract FFmpeg
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall("temp_ffmpeg")
        
        # Find the extracted directory
        extracted_dir = None
        for item in os.listdir("temp_ffmpeg"):
            if item.startswith("ffmpeg-master"):
                extracted_dir = os.path.join("temp_ffmpeg", item)
                break
        
        if not extracted_dir:
            raise Exception("Could not find FFmpeg directory in extracted files")
        
        # Copy FFmpeg files to project directory
        import shutil
        ffmpeg_bin_dir = os.path.join(extracted_dir, "bin")
        for file in os.listdir(ffmpeg_bin_dir):
            if file.endswith('.exe'):
                src = os.path.join(ffmpeg_bin_dir, file)
                dst = os.path.join(ffmpeg_dir, file)
                shutil.copy2(src, dst)
                print(f"Installed: {file}")
        
        # Clean up
        os.remove(zip_filename)
        shutil.rmtree("temp_ffmpeg")
        
        print(f"\n✅ FFmpeg installed successfully in: {ffmpeg_dir}")
        print("FFmpeg binaries:")
        for file in os.listdir(ffmpeg_dir):
            print(f"  - {file}")
        
        return str(ffmpeg_dir)
        
    except Exception as e:
        print(f"❌ Error installing FFmpeg: {e}")
        return None

def check_ffmpeg():
    """Check if FFmpeg is available."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def main():
    """Main installation function."""
    print("FFmpeg Installer for YouTube Downloader")
    print("=" * 40)
    
    # Check if FFmpeg is already installed
    if check_ffmpeg():
        print("✅ FFmpeg is already installed and available in PATH")
        return
    
    # Check if FFmpeg exists in project directory
    project_dir = Path(__file__).parent
    ffmpeg_dir = project_dir / "ffmpeg"
    
    if ffmpeg_dir.exists() and any(ffmpeg_dir.glob("*.exe")):
        print("✅ FFmpeg found in project directory")
        return
    
    # Install FFmpeg
    print("FFmpeg not found. Installing...")
    ffmpeg_path = install_ffmpeg()
    
    if ffmpeg_path:
        print(f"\n🎉 FFmpeg installation complete!")
        print(f"Location: {ffmpeg_path}")
        print("\nThe YouTube downloader will now use the local FFmpeg installation.")
    else:
        print("\n❌ FFmpeg installation failed.")
        print("You can still use the downloader, but some features may be limited.")

if __name__ == "__main__":
    main() 