#!/usr/bin/env python3
"""
Script to create and push tags manually when GitHub Actions fails.
This is a fallback solution for tag creation issues.
"""

import subprocess
import sys
import os
import re
from datetime import datetime

def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.stderr.strip(), e.returncode

def get_current_version():
    """Get the current version from the latest tag."""
    stdout, stderr, returncode = run_command("git describe --tags --abbrev=0", check=False)
    if returncode == 0:
        # Extract version from tag like "v1.2.3"
        match = re.search(r'v(\d+\.\d+\.\d+)', stdout)
        if match:
            return match.group(1)
    
    # If no tags exist, start with v0.1.0
    return "0.0.0"

def calculate_new_version(current_version, bump_type):
    """Calculate new version based on bump type."""
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        return f"{major}.{minor}.{patch + 1}"

def create_tag(version, message=None):
    """Create and push a new tag."""
    tag_name = f"v{version}"
    
    if not message:
        message = f"Release {tag_name}"
    
    print(f"Creating tag: {tag_name}")
    print(f"Message: {message}")
    
    # Create the tag
    stdout, stderr, returncode = run_command(f'git tag -a "{tag_name}" -m "{message}"')
    if returncode != 0:
        print(f"Error creating tag: {stderr}")
        return False
    
    # Push the tag
    stdout, stderr, returncode = run_command(f'git push origin "{tag_name}"')
    if returncode != 0:
        print(f"Error pushing tag: {stderr}")
        print("\nTo push manually, run:")
        print(f"git push origin {tag_name}")
        return False
    
    print(f"✅ Successfully created and pushed tag: {tag_name}")
    return True

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python create_tag.py <version> [message]")
        print("Examples:")
        print("  python create_tag.py 0.1.0")
        print("  python create_tag.py 0.1.0 'Initial release'")
        print("  python create_tag.py patch 'Bug fix release'")
        print("  python create_tag.py minor 'New feature release'")
        print("  python create_tag.py major 'Breaking change release'")
        sys.exit(1)
    
    version_arg = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if we're in a git repository
    stdout, stderr, returncode = run_command("git status", check=False)
    if returncode != 0:
        print("Error: Not in a git repository")
        sys.exit(1)
    
    # Handle special version keywords
    if version_arg in ["patch", "minor", "major"]:
        current_version = get_current_version()
        new_version = calculate_new_version(current_version, version_arg)
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
        version = new_version
    else:
        # Validate version format
        if not re.match(r'^\d+\.\d+\.\d+$', version_arg):
            print("Error: Version must be in format X.Y.Z (e.g., 0.1.0)")
            sys.exit(1)
        version = version_arg
    
    # Create the tag
    success = create_tag(version, message)
    if success:
        print(f"\n🎉 Tag v{version} created successfully!")
        print(f"GitHub Actions should now trigger the release workflow.")
    else:
        print(f"\n❌ Failed to create tag v{version}")
        sys.exit(1)

if __name__ == "__main__":
    main() 