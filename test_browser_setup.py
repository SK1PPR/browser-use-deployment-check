#!/usr/bin/env python3
"""
Test script to verify browser setup for cloud deployment.
"""

import os
import sys
import platform
from pathlib import Path

def test_environment_setup():
    """Test environment setup."""
    print("🔧 Testing environment setup...")
    
    system = platform.system()
    print(f"Platform: {system}")
    
    if system == 'Linux':
        # Check if cache directory exists
        cache_dir = '/home/appuser/.cache/ms-playwright'
        if os.path.exists(cache_dir):
            print(f"✅ Cache directory exists: {cache_dir}")
        else:
            print(f"❌ Cache directory missing: {cache_dir}")
            return False
        
        # Check environment variables
        browsers_path = os.environ.get('PLAYWRIGHT_BROWSERS_PATH')
        if browsers_path:
            print(f"✅ PLAYWRIGHT_BROWSERS_PATH set: {browsers_path}")
        else:
            print("❌ PLAYWRIGHT_BROWSERS_PATH not set")
            return False
    
    print("✅ Environment setup test passed")
    return True

def test_browser_installation():
    """Test browser installation."""
    print("🔧 Testing browser installation...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Try to launch chromium
            browser = p.chromium.launch(headless=True)
            browser.close()
            print("✅ Browser installation test passed")
            return True
    except Exception as e:
        print(f"❌ Browser installation test failed: {e}")
        return False

def test_browser_use_import():
    """Test browser-use import."""
    print("🔧 Testing browser-use import...")
    
    try:
        from browser_use import Agent, BrowserProfile
        print("✅ browser-use import test passed")
        return True
    except Exception as e:
        print(f"❌ browser-use import test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running browser setup tests...")
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Browser Installation", test_browser_installation),
        ("Browser-Use Import", test_browser_use_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Browser setup is ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please check the setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 