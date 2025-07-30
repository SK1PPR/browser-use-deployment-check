#!/usr/bin/env python3
"""
Setup script for Playwright browsers in cloud deployment.
This script ensures browsers are properly installed before the app starts.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def install_playwright_browsers():
    """Install Playwright browsers for the current platform."""
    print("🔧 Installing Playwright browsers...")
    
    try:
        # Install browsers with force flag
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium", "--force"
        ], capture_output=True, text=True, check=True)
        
        print("✅ Playwright browsers installed successfully!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install browsers: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_environment():
    """Setup environment for cloud deployment."""
    system = platform.system()
    
    if system == 'Linux':
        # Set environment variables for cloud deployment
        os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/appuser/.cache/ms-playwright')
        os.environ.setdefault('PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD', '0')
        
        # Ensure the cache directory exists
        cache_dir = '/home/appuser/.cache/ms-playwright'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
            print(f"✅ Created cache directory: {cache_dir}")
        
        print("ℹ️  Environment set up for Linux cloud deployment")
    
    elif system == 'Darwin':  # macOS
        # Use local cache if it exists
        local_cache = Path('/Users/khushalagrawal/Library/Caches/ms-playwright')
        if local_cache.exists():
            os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(local_cache))
            print(f"✅ Using local Playwright cache: {local_cache}")
        else:
            print("ℹ️  Using default Playwright browser paths for macOS")
    
    else:
        print(f"ℹ️  Using default Playwright browser paths for {system}")

def verify_installation():
    """Verify that browsers are properly installed."""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Try to launch chromium
            browser = p.chromium.launch(headless=True)
            browser.close()
            print("✅ Browser installation verified successfully!")
            return True
    except Exception as e:
        print(f"❌ Browser installation verification failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Playwright browsers for deployment...")
    
    # Setup environment
    setup_environment()
    
    # Install browsers
    if not install_playwright_browsers():
        print("❌ Failed to install browsers")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("❌ Browser verification failed")
        sys.exit(1)
    
    print("✅ Setup completed successfully!")

if __name__ == "__main__":
    main() 