"""
Basic tests for Baresha Downloader
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests"""

    def test_imports(self):
        """Test that required modules can be imported"""
        try:
            import yt_dlp
            import PIL
            import requests
            import tkinter

            self.assertTrue(True, "All required modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import required module: {e}")

    def test_python_version(self):
        """Test that Python version is supported"""
        self.assertGreaterEqual(sys.version_info[:2], (3, 8), "Python 3.8 or higher is required")

    def test_main_module_exists(self):
        """Test that the main module file exists"""
        main_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "youtube_downloader.py")
        self.assertTrue(os.path.exists(main_file), "Main module youtube_downloader.py should exist")

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists"""
        req_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "requirements.txt")
        self.assertTrue(os.path.exists(req_file), "requirements.txt should exist")


if __name__ == "__main__":
    unittest.main()
