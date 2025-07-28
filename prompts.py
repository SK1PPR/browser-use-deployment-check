# Centralized prompts for the Workflow Automator

# --------- Step Breakdown Prompt ---------
STEP_BREAKDOWN_PROMPT = """
You are a screener automation agent specialized in stock market analysis and financial data extraction. 
Given the following user request, break it down into 3-8 clear, actionable steps that a browser automation agent can follow.
Each step should be specific and executable for stock screening tasks.

User Request: {user_request}

Please format your response as a numbered list of steps. Each step should be clear and actionable for stock screening.
Example format for stock screening tasks:
1. Navigate to screener.in and access the stock screener
2. Set P/E ratio filter to less than 15
3. Set market cap filter to above 1000cr
4. Apply filters and view the filtered results
5. Export or analyze the filtered stock list

Focus on steps that involve:
- Navigating to financial screening websites
- Setting up filters (P/E ratio, market cap, sector, etc.)
- Applying filters and viewing results
- Extracting or analyzing stock data
- Exporting results if needed

Steps:
"""

# --------- Step Combination Prompt ---------
STEP_COMBINATION_PROMPT = """
You are a screener automation agent. Take the following original request and approved steps, and create a comprehensive, detailed prompt that a browser automation agent can execute.

Original Request: {original_request}

Approved Steps:
{approved_steps}

Create a detailed, actionable prompt that:
1. Clearly states the objective
2. Provides specific instructions for each step
3. Includes any necessary details about filters, criteria, or actions
4. Is written in a way that a browser automation agent can understand and execute
5. Maintains the context of stock screening and financial analysis
6. Explicitly instructs the agent to keep the browser open and wait for user review
7. Includes a final step to pause and wait for user confirmation before closing

The prompt should be comprehensive enough that the browser agent can execute it without needing additional clarification.
IMPORTANT: The agent should NOT close the browser automatically. It should keep the browser open for user review.

Combined Prompt:
"""

# --------- Authentication Messages ---------
LOGIN_WELCOME = "🔐 Welcome to Screener.in Workflow Automator"
LOGIN_INSTRUCTIONS = "Please log in to access the stock screening automation system."
LOGIN_HEADER = "User Authentication"
LOGIN_USERNAME_LABEL = "Username"
LOGIN_USERNAME_HELP = "Enter your username"
LOGIN_PASSWORD_LABEL = "Password"
LOGIN_PASSWORD_HELP = "Enter your password"
LOGIN_BUTTON = "Login"
LOGIN_ERROR = "Invalid username or password. Please try again."
LOGIN_SUCCESS = "Login successful! Welcome to the system."

# --------- Credentials Setup Messages ---------
CREDENTIALS_WELCOME = "🔐 Welcome to Screener.in Workflow Automator"
CREDENTIALS_INSTRUCTIONS = "Please configure your Screener.in credentials to get started with stock screening automation."
CREDENTIALS_HEADER = "Enter Your Screener.in Credentials"
CREDENTIALS_EMAIL_LABEL = "Screener.in Email Address"
CREDENTIALS_EMAIL_HELP = "Enter your email address used for Screener.in account"
CREDENTIALS_PASSWORD_LABEL = "Screener.in Password"
CREDENTIALS_PASSWORD_HELP = "Enter your password for Screener.in account"
CREDENTIALS_SAVE_BUTTON = "Save Screener.in Credentials"
CREDENTIALS_SUCCESS = "Screener.in credentials saved successfully! You can now use the stock screening automation."
CREDENTIALS_ERROR = "Please fill in all required fields."

# --------- UI Messages ---------
WORKFLOW_TITLE = "📊 Workflow Automator"
START_WORKFLOW_HEADER = "🚀 Start Your Workflow"
START_WORKFLOW_DESCRIPTION = "Enter your workflow prompt below and we'll break it down into actionable steps."
WORKFLOW_INPUT_PLACEHOLDER = "e.g., Find stocks with P/E ratio less than 15 and market cap above 1000cr"
BREAK_DOWN_BUTTON = "📋 Break Down Steps"
STEP_BREAKDOWN_TITLE = "📋 Workflow Step Breakdown"
PROPOSED_STEPS_HEADER = "📝 Proposed Steps"
APPROVE_RUN_BUTTON = "✅ Approve & Run"
REJECT_MODIFY_BUTTON = "❌ Reject & Modify"
EXECUTE_WORKFLOW_BUTTON = "🚀 Execute Workflow"
AGENT_THOUGHTS_HEADER = "Agent's Thoughts"
BROWSER_SCREENSHOT_HEADER = "Browser Screenshot"

# --------- Status Messages ---------
AGENT_RUNNING = "🔄 Agent is running..."
AGENT_COMPLETED = "✅ Agent execution completed successfully!"
AGENT_FAILED = "❌ Agent execution failed"
BROWSER_KEEP_OPEN = "The browser will remain open so you can review the results. Close it manually when done."
WORKFLOW_STARTING = "🚀 Starting workflow execution..."
EXECUTION_PROMPT_TITLE = "📋 Execution Prompt (Generated from Steps)"
EXECUTION_PROMPT_DESCRIPTION = "This is the comprehensive prompt that will be sent to the browser automation agent."

# --------- Error Messages ---------
ERROR_BREAKDOWN = "Error breaking down prompt: {error}"
ERROR_COMBINE_STEPS = "Error combining steps: {error}"
ERROR_CREATE_AGENT = "Failed to create agent: {error}"
ERROR_AGENT_EXECUTION = "Agent execution failed: {error}"
ERROR_CRITICAL = "Critical error in agent execution: {error}"
ERROR_START_WORKFLOW = "Failed to start workflow: {error}"
ERROR_RUN_AGENT = "Failed to run agent: {error}"
ERROR_SCREENSHOT = "Screenshot capture failed: {error}"
ERROR_UPDATE_THOUGHTS = "Error updating thoughts: {error}"
ERROR_DISPLAY_THOUGHTS = "Error displaying final thoughts: {error}"

# --------- Debug Messages ---------
DEBUG_TITLE = "🔍 Debug Information"
DEBUG_SESSION_STATE = "Session State Keys:"
DEBUG_ENVIRONMENT = "Environment:"
DEBUG_WORKING_DIR = "Working directory: {dir}"
DEBUG_SCREENSHOTS_EXIST = "Screenshots directory exists: {exists}"
DEBUG_BROWSER_TEST = "🧪 Test Browser"
DEBUG_BROWSER_TESTING = "Testing browser automation..."
DEBUG_BROWSER_SUCCESS = "Browser test successful!"
DEBUG_BROWSER_FAILED = "Browser test failed: {error}"

# --------- Navigation Messages ---------
BACK_TO_INPUT = "← Back to Input"
RECONFIGURE_CREDENTIALS = "🔧 Reconfigure Screener.in Credentials"
LOGOUT_BUTTON = "🚪 Logout"
RESET_WORKFLOW = "🔄 Reset Workflow"
BACK_TO_STEP_BREAKDOWN = "← Back to Step Breakdown"
ADD_NEW_STEP = "➕ Add New Step"
EDIT_STEP_TITLE = "✏️ Edit Step"
SAVE_BUTTON = "💾 Save"
CANCEL_BUTTON = "❌ Cancel"
RESET_ERROR_STATE = "🔄 Reset Error State"

# --------- Agent Configuration ---------
AGENT_TASK_PREFIX = "Execute the following stock screening task: {task}. Steps: {steps}" 