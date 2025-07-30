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



# --------- File Paths ---------
SCREENSHOTS_DIR = 'screenshots'
SCREENSHOT_FILENAME = 'screenshot.png'
STEP_SCREENSHOT_FORMAT = 'step_{}.png'

# --------- Session State Keys ---------
SESSION_KEYS = {
    'authenticated': False,
    'login_error': "",
    'latest_thoughts': "",
    'agent_ran': False,
    'agent_completed': False,
    'final_result': "",
    'start_realtime_updates': False,
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

# Set Playwright environment variables for cloud deployment
# Use platform-agnostic paths that work on both local and cloud deployments
import platform

# For cloud deployment, let Playwright use its default paths
# For local development, we can optionally set a custom path
if platform.system() == 'Darwin':  # macOS
    # Only set custom path for local development if it exists
    local_cache_path = '/Users/khushalagrawal/Library/Caches/ms-playwright'
    if os.path.exists(local_cache_path):
        os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', local_cache_path)
else:
    # On cloud deployments (Linux), use default paths
    # Let Playwright manage its own browser installation
    pass

# Ensure browsers are downloaded
os.environ.setdefault('PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD', '0')

# --------- Debug Configuration ---------
DEBUG_MODE = get_env_var('DEBUG_MODE', 'False').lower() == 'true'
LOG_LEVEL = get_env_var('LOG_LEVEL', 'INFO') 