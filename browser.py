from browser_use import Agent, BrowserProfile
from browser_use.llm import ChatOpenAI
import base64
from prompts import BROWSER_AUTOMATION_PROMPT
from config import LLM_MODEL
import streamlit as st
from browser_setup import setup_browser_environment, get_browser_profile_args
import platform

llm = ChatOpenAI(model=LLM_MODEL)

# Setup browser environment with error handling
try:
    setup_browser_environment()
except Exception as e:
    st.error(f"Browser setup failed: {e}")
    print(f"Browser setup error: {e}")

# Get browser profile arguments with platform-specific optimizations
browser_args = get_browser_profile_args()

# Add additional arguments for cloud deployment
if platform.system() == 'Linux':
    browser_args.extend([
        '--disable-dev-shm-usage',
        '--disable-gpu-sandbox',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-renderer-backgrounding',
        '--disable-features=VizDisplayCompositor',
        '--disable-ipc-flooding-protection',
        '--single-process',
        '--no-zygote',
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
        '--disable-features=TranslateUI'
    ])

custom_browser_profile = BrowserProfile(
    headless=True, 
    args=browser_args,
    # Set a large window size to ensure full page capture
    window_size={"width": 1920, "height": 1080},
    # Remove viewport constraint to allow full page screenshots
    # viewport={"width": 1200, "height": 800}
)

async def on_step_start_hook(agent: Agent):
    """Hook function that captures and records agent activity at each step start."""
    # Get step number from session state
    step_counter = st.session_state.get('step_counter', {'n': 0})
    step_num = step_counter['n'] + 1
    st.session_state['step_counter']['n'] = step_num

    # Capture screenshot
    try:
        website_screenshot = await agent.browser_session.take_screenshot(full_page=True)
        screenshot_bytes = base64.b64decode(website_screenshot)
        if 'screenshots' not in st.session_state:
            st.session_state['screenshots'] = []
        st.session_state['screenshots'].append(screenshot_bytes)
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
        website_screenshot = await agent.browser_session.take_screenshot(full_page=True)
        screenshot_bytes = base64.b64decode(website_screenshot)
        if 'screenshots' not in st.session_state:
            st.session_state['screenshots'] = []
        st.session_state['screenshots'].append(screenshot_bytes)
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        # Continue without screenshot
    st.session_state['step_counter']['n'] = step_num

def cleanup_screenshots():
    """Reset screenshots in session state and reset step counter."""
    st.session_state['screenshots'] = []
    st.session_state['step_counter'] = {'n': 0}

async def execute_workflow(query):
    """Execute the workflow using the browser automation agent."""
    # Create agent with simplified configuration

    prompt = BROWSER_AUTOMATION_PROMPT.format(prompt=query)
    
    try:
        agent = Agent(
            task=prompt,
            llm=llm,
            sensitive_data={
                'https://www.screener.in/': {
                    'email': st.session_state['sensitive_data']['email'],
                    'password': st.session_state['sensitive_data']['password']
                }
            },
            browser_profile=custom_browser_profile
        )

        # Initialize session state for live updates
        if 'latest_thoughts' not in st.session_state:
            st.session_state['latest_thoughts'] = ""
        st.session_state['agent_ran'] = True
        st.session_state['agent_completed'] = False
        st.session_state['start_realtime_updates'] = True
        
        result = await agent.run(on_step_start=on_step_start_hook, on_step_end=on_step_end_hook)
        st.session_state['latest_thoughts'] += f"\n\n**Workflow completed successfully!**"
        st.session_state['agent_completed'] = True
        st.session_state['start_realtime_updates'] = False
        st.session_state['final_result'] = result.final_result()
        return result
        
    except Exception as e:
        st.session_state['latest_thoughts'] += f"\n\n**Error during execution: {str(e)}**"
        st.session_state['agent_error'] = True
        st.session_state['agent_completed'] = True
        st.session_state['start_realtime_updates'] = False
        st.session_state['final_result'] = f"Error: {str(e)}"
        raise e