# Configuration settings for the Workflow Automator

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --------- App Configuration ---------
APP_TITLE = "Workflow Automator"
APP_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "collapsed"

# --------- LLM Configuration ---------
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.0

# --------- Browser Configuration ---------
BROWSER_HEADLESS = False
BROWSER_KEEP_ALIVE = True
BROWSER_CONFIG = {
    "keep_alive": True,
    "headless": False
}

# --------- Initial Actions ---------
INITIAL_ACTIONS = [
    {
        'open_tab': {
            'url': 'https://screener.in/',
        }
    }
]

# --------- File Paths ---------
SCREENSHOTS_DIR = 'screenshots'
SCREENSHOT_FILENAME = 'screenshot.png'
STEP_SCREENSHOT_FORMAT = 'step_{}.png'

# --------- Session State Keys ---------
SESSION_KEYS = {
    'latest_thoughts': "",
    'agent_ran': False,
    'credentials_configured': False,
    'sensitive_data': {},
    'workflow_steps': [],
    'workflow_approved': False,
    'current_prompt': "",
    'show_workflow_view': False,
    'editing_step': None,
    'edited_steps': [],
    'agent_error': False,
    'combined_prompt': "",
    'step_counter': {'n': 0}
}

# --------- UI Layout ---------
COLUMN_RATIOS = {
    'main': [1, 2, 1],  # For centering content
    'workflow': [1, 2],  # For workflow execution view
    'approval': [1, 2, 1],  # For approval buttons
    'step_actions': [0.5, 4, 1, 1]  # For step list (number, text, edit, delete)
}

# --------- Environment Variables ---------
def get_env_var(key, default=None):
    """Get environment variable with fallback to default."""
    return os.getenv(key, default)

# --------- Debug Configuration ---------
DEBUG_MODE = get_env_var('DEBUG_MODE', 'False').lower() == 'true'
LOG_LEVEL = get_env_var('LOG_LEVEL', 'INFO') 