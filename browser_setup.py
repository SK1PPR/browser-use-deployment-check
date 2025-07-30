#!/usr/bin/env python3
"""
Browser setup module for Playwright configuration.
Handles browser installation and platform-specific configurations.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

def force_install_playwright_browsers():
    """Force install Playwright browsers for the current platform."""
    print("🔧 Installing Playwright browsers...")
    
    try:
        # Force install browsers with explicit path for cloud deployment
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

def setup_playwright_environment():
    """Setup Playwright environment variables for the current platform."""
    
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        # Use local cache if it exists, otherwise let Playwright use defaults
        local_cache = Path('/Users/khushalagrawal/Library/Caches/ms-playwright')
        if local_cache.exists():
            os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(local_cache))
            print(f"✅ Using local Playwright cache: {local_cache}")
        else:
            print("ℹ️  Using default Playwright browser paths")
    
    elif system == 'Linux':
        # On Linux (cloud deployment), set specific paths and force install
        print("ℹ️  Setting up Playwright for Linux cloud deployment")
        
        # Set environment variables for cloud deployment
        os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/home/appuser/.cache/ms-playwright')
        os.environ.setdefault('PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD', '0')
        
        # Force install browsers for cloud deployment
        if not force_install_playwright_browsers():
            print("❌ Failed to install browsers for cloud deployment")
            return False
    
    else:
        # Windows or other platforms
        print(f"ℹ️  Using default Playwright browser paths for {system}")
    
    # Ensure browsers are downloaded
    os.environ.setdefault('PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD', '0')

def get_browser_profile_args():
    """Get browser profile arguments based on the platform."""
    system = platform.system()
    
    base_args = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-web-security',
        '--disable-extensions',
        '--disable-plugins'
    ]
    
    if system == 'Linux':
        # Additional args for Linux/cloud deployment
        base_args.extend([
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=VizDisplayCompositor',
            '--disable-ipc-flooding-protection',
            '--single-process',  # Use single process for cloud deployment
            '--no-zygote',  # Disable zygote process
            '--disable-setuid-sandbox',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--mute-audio',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--disable-client-side-phishing-detection',
            '--disable-component-update',
            '--disable-domain-reliability',
            '--disable-features=AudioServiceOutOfProcess',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection'
        ])
    
    return base_args

def setup_browser_environment():
    """Complete browser environment setup."""
    print("🔧 Setting up browser environment...")
    
    # Setup environment variables
    setup_playwright_environment()
    
    # Force install browsers for cloud deployment
    if platform.system() == 'Linux':
        if not force_install_playwright_browsers():
            print("❌ Failed to install browsers for cloud deployment")
            return False
    
    print("✅ Browser environment setup complete")
    return True

def verify_browser_installation():
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

if __name__ == "__main__":
    setup_browser_environment()
    verify_browser_installation() 