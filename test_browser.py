#!/usr/bin/env python3
"""
Test script to verify Playwright browser installation.
"""

import asyncio
from playwright.async_api import async_playwright
from browser_setup import setup_browser_environment

async def test_browser():
    """Test if browser can be launched successfully."""
    print("🧪 Testing browser installation...")
    
    # Setup browser environment
    setup_browser_environment()
    
    try:
        async with async_playwright() as p:
            # Try to launch browser
            browser = await p.chromium.launch(headless=True)
            print("✅ Browser launched successfully!")
            
            # Try to create a page
            page = await browser.new_page()
            print("✅ Page created successfully!")
            
            # Try to navigate to a simple page
            await page.goto('https://example.com')
            print("✅ Navigation successful!")
            
            # Try to take a screenshot
            screenshot = await page.screenshot()
            print("✅ Screenshot taken successfully!")
            
            await browser.close()
            print("✅ Browser closed successfully!")
            
            return True
            
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_browser())
    if success:
        print("🎉 All browser tests passed!")
    else:
        print("💥 Browser tests failed!")
        exit(1) 