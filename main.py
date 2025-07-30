# Main application file for the Workflow Automator
# This is the modular version that imports from separate files

import streamlit as st
import asyncio
import nest_asyncio
import os
import platform

# Import our modular components
from config import *
from prompts import *
from session_manager import SessionManager
from ui_components import UIComponents

# Allow nested async loops
nest_asyncio.apply()

# Run browser setup for cloud deployment
if platform.system() == 'Linux':
    try:
        from setup_browsers import setup_environment, install_playwright_browsers, verify_installation
        
        # Setup environment
        setup_environment()
        
        # Install browsers if not already installed
        if not verify_installation():
            print("Installing Playwright browsers...")
            install_playwright_browsers()
    except Exception as e:
        st.error(f"Browser setup failed: {e}")

# Initialize session state
SessionManager.initialize_session_state()

# Setup page configuration
UIComponents.setup_page()

# --------- Main App Logic ---------
# Check authentication first
if not st.session_state['authenticated']:
    UIComponents.authenticate_user()
else:
    # Check for Screener.in credentials setup
    if not st.session_state['credentials_configured']:
        UIComponents.credentials_setup()
    else:
        # --------- Full Screen Step Breakdown View ---------
        if st.session_state['workflow_steps'] and not st.session_state['workflow_approved']:
            UIComponents.step_breakdown_view()
        
        # --------- Workflow Execution View ---------
        elif st.session_state['show_workflow_view']:
            UIComponents.workflow_execution_view()
        
        # --------- Initial Input View ---------
        else:
            UIComponents.initial_input_view() 