from browser_use import Agent, BrowserSession, BrowserProfile
import os
import base64
from langchain_openai import ChatOpenAI
from config import LLM_MODEL, INITIAL_ACTIONS
from prompts import AGENT_RUNNING, AGENT_COMPLETED
import streamlit as st
import shutil

llm = ChatOpenAI(model=LLM_MODEL)

custom_browser_profile = BrowserProfile(headless=False)

async def on_step_start_hook(agent: Agent):
    """Hook function that captures and records agent activity at each step start."""
    # Ensure screenshots directory exists
    screenshots_dir = 'screenshots'
    os.makedirs(screenshots_dir, exist_ok=True)

    # Get step number from session state
    step_counter = st.session_state.get('step_counter', {'n': 0})
    step_num = step_counter['n'] + 1
    st.session_state['step_counter']['n'] = step_num

    # Capture screenshot
    try:
        website_screenshot = await agent.browser_session.take_screenshot()
        
        # Save screenshot to file - decode base64 string to bytes
        screenshot_path = os.path.join(screenshots_dir, f"step_{step_num}.png")
        screenshot_bytes = base64.b64decode(website_screenshot)
        with open(screenshot_path, "wb") as f:
            f.write(screenshot_bytes)
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        # Continue without screenshot

    # Get the current action being performed
    try:
        thoughts = agent.state.history.model_thoughts()
        if thoughts and len(thoughts) > 0:
            current_action = thoughts[-1].next_goal
        else:
            current_action = "Starting step"
    except Exception as e:
        print(f"Error getting current action: {e}")
        current_action = "Starting step"
    
    # Update session state with live action
    if 'latest_thoughts' not in st.session_state:
        st.session_state['latest_thoughts'] = ""
    
    # Add new step action to thoughts with timestamp
    step_action = f"**Step {step_num} Started:** {current_action}\n\n"
    st.session_state['latest_thoughts'] += step_action
    

async def on_step_end_hook(agent: Agent):
    """Hook function that captures and records agent activity at each step end."""

    # Get step number from session state
    step_counter = st.session_state.get('step_counter', {'n': 0})
    step_num = step_counter['n']
    st.session_state['step_counter']['n'] = step_num

    # Capture screenshot
    try:
        website_screenshot = await agent.browser_session.take_screenshot()
        
        # Save screenshot to file - decode base64 string to bytes
        screenshot_path = os.path.join('screenshots', f"step_{step_num}.png")
        screenshot_bytes = base64.b64decode(website_screenshot)
        with open(screenshot_path, "wb") as f:
            f.write(screenshot_bytes)
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        # Continue without screenshot

    st.session_state['step_counter']['n'] = step_num

def cleanup_screenshots():
        """Clean up screenshots directory and reset step counter."""
        screenshots_dir = 'screenshots'
        if os.path.exists(screenshots_dir):
            shutil.rmtree(screenshots_dir)
        os.makedirs(screenshots_dir, exist_ok=True)
        st.session_state['step_counter'] = {'n': 0} 

async def execute_workflow(query):
    """Execute the workflow using the browser automation agent."""

    # Create agent with simplified configuration
    agent = Agent(
        task=query,
        llm=llm,
        sensitive_data={
            'https://www.screener.in/': {
                'email': st.session_state['sensitive_data']['email'],
                'password': st.session_state['sensitive_data']['password']
            }
        },
        initial_actions=INITIAL_ACTIONS,
        browser_profile=custom_browser_profile
    )

    # Initialize session state for live updates
    if 'latest_thoughts' not in st.session_state:
        st.session_state['latest_thoughts'] = ""
    st.session_state['agent_ran'] = True
    
    result = await agent.run(on_step_start=on_step_start_hook, on_step_end=on_step_end_hook)
    return result