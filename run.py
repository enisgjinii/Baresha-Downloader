#!/usr/bin/env python3
"""
Simple launcher for the YouTube Video Downloader
"""

import sys
import os
import subprocess


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import yt_dlp
        import requests
        from PIL import Image
        import tkinter

        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False


def main():
    """Main launcher function."""
    print("YouTube Video Downloader")
    print("=" * 30)

    # Check dependencies
    if not check_dependencies():
        return 1

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloader_script = os.path.join(script_dir, "youtube_downloader.py")

    # Check if the main script exists
    if not os.path.exists(downloader_script):
        print(f"Error: {downloader_script} not found!")
        return 1

    # Pass all arguments to the main script
    args = [sys.executable, downloader_script] + sys.argv[1:]

    try:
        # Run the main script
        result = subprocess.run(args, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running downloader: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
