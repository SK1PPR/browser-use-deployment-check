from browser_use import Agent
import os
from langchain_openai import ChatOpenAI
from config import LLM_MODEL, INITIAL_ACTIONS
from prompts import AGENT_RUNNING, AGENT_COMPLETED
import streamlit as st
import shutil

llm = ChatOpenAI(model=LLM_MODEL)

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
    website_screenshot = await agent.browser_session.take_screenshot()

    # Save screenshot to file
    screenshot_path = os.path.join(screenshots_dir, f"step_{step_num}.png")
    with open(screenshot_path, "wb") as f:
        f.write(website_screenshot)

    if 'screenshot_placeholder' in st.session_state:
        st.session_state['screenshot_placeholder'].image(
            website_screenshot, caption=f"Step {step_num} Screenshot", use_column_width=True
        )

async def on_step_end_hook(agent: Agent):
    """Hook function that captures and records agent activity at each step end."""

    # Get step number from session state
    step_counter = st.session_state.get('step_counter', {'n': 0})
    step_num = step_counter['n'] + 1
    st.session_state['step_counter']['n'] = step_num

    # Capture screenshot
    website_screenshot = await agent.browser_session.take_screenshot()

    # Save screenshot to file
    screenshot_path = os.path.join('screenshots', f"step_{step_num}.png")
    with open(screenshot_path, "wb") as f:
        f.write(website_screenshot)

    if 'screenshot_placeholder' in st.session_state:
        st.session_state['screenshot_placeholder'].image(
            website_screenshot, caption=f"Step {step_num} Screenshot", use_column_width=True
        )

    st.session_state['step_counter']['n'] = step_num

def cleanup_screenshots():
        """Clean up screenshots directory and reset step counter."""
        screenshots_dir = 'screenshots'
        if os.path.exists(screenshots_dir):
            shutil.rmtree(screenshots_dir)
        os.makedirs(screenshots_dir, exist_ok=True)
        st.session_state['step_counter'] = {'n': 0} 

async def execute_workflow(query, thoughts_placeholder, screenshot_placeholder):
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
        initial_actions=INITIAL_ACTIONS
    )

    # Run agent with simple approach
    print(f"\n🚀 Running the task: {query}\n")
    
    # Update UI before starting
    with thoughts_placeholder.expander("Agent Status", expanded=True):
        st.markdown(f"**{AGENT_RUNNING}**")
        st.markdown(f"**Task:** {query}")
    
    # Simple agent run without complex callbacks
    result = await agent.run()
    
    # Update UI after completion
    with thoughts_placeholder.expander("Agent Status", expanded=True):
        st.markdown(f"**{AGENT_COMPLETED}**")
        st.markdown(f"**Task:** {query}")
    
    # Show extracted content if available
    if hasattr(result, 'extracted_content') and result.extracted_content():
        with thoughts_placeholder.expander("Extracted Content", expanded=True):
            st.markdown(result.extracted_content())