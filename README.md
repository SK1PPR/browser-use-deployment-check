# Screener.in Workflow Automator - Modular Version

A Streamlit application that automates stock screening workflows by breaking down user prompts into actionable steps using an LLM, showing these steps for user approval, and then running a browser automation agent for Screener.in.

## 🔐 Authentication

The application requires user authentication before accessing the stock screening features. Set the following environment variables:

```bash
# Required: User authentication
APP_USERNAME=your_username_here
APP_PASSWORD=your_password_here

# Optional: Debug configuration
DEBUG_MODE=False
LOG_LEVEL=INFO
```

## 📁 Project Structure

## 📁 Project Structure

The application has been refactored into a modular structure for better maintainability:

```
server/
├── main.py              # Original monolithic file (kept for reference)
├── main_new.py          # New modular main file
├── prompts.py           # All prompts and UI messages
├── config.py            # Configuration settings and constants
├── agent_manager.py     # Browser automation agent logic
├── ui_components.py     # Streamlit UI components
├── session_manager.py   # Session state management
└── README.md           # This file
```

## 🔧 Files Overview

### `prompts.py` - Centralized Prompt Management
**Purpose**: Contains all LLM prompts and UI messages in one place for easy modification.

**Key Sections**:
- `STEP_BREAKDOWN_PROMPT` - LLM prompt for breaking down user requests into steps
- `STEP_COMBINATION_PROMPT` - LLM prompt for combining approved steps into execution prompt
- UI Messages - All button labels, titles, and status messages
- Error Messages - Centralized error handling messages

**To Modify Prompts**: Simply edit the variables in this file. No need to search through the main code.

### `config.py` - Application Configuration
**Purpose**: Centralized configuration for all app settings.

**Key Sections**:
- App configuration (title, layout, sidebar state)
- LLM configuration (model, temperature)
- Browser configuration (headless, keep_alive)
- File paths and session state keys
- UI layout ratios

**To Change Settings**: Modify the constants in this file.

### `agent_manager.py` - Browser Automation Logic
**Purpose**: Handles all browser automation operations.

**Key Features**:
- `AgentManager` class with methods for:
  - Breaking down prompts into steps
  - Combining steps into execution prompts
  - Executing workflows with browser automation
  - Screenshot cleanup

### `ui_components.py` - Streamlit UI Components
**Purpose**: Manages all Streamlit interface elements.

**Key Components**:
- `UIComponents` class with static methods for:
  - Page setup and configuration
  - Credentials setup form
  - Initial input view
  - Step breakdown view
  - Workflow execution view

### `session_manager.py` - Session State Management
**Purpose**: Handles Streamlit session state initialization and operations.

**Key Features**:
- Session state initialization
- State reset operations
- Placeholder management
- Debug information

### `main_new.py` - Modular Main Application
**Purpose**: Clean, simple main file that orchestrates all components.

**Key Features**:
- Imports all modular components
- Simple flow control
- Minimal code duplication

## 🚀 Usage

### Setup

1. **Set environment variables** for authentication:
   ```bash
   export APP_USERNAME=your_username_here
   export APP_PASSWORD=your_password_here
   ```

2. **Create a .env file** (optional but recommended):
   ```bash
   APP_USERNAME=your_username_here
   APP_PASSWORD=your_password_here
   DEBUG_MODE=False
   LOG_LEVEL=INFO
   ```

### Running the Application

1. **Use the modular version** (recommended):
   ```bash
   streamlit run main_new.py
   ```

2. **Use the original version** (for reference):
   ```bash
   streamlit run main.py
   ```

### Authentication Flow

1. **Login Page**: Users must authenticate with username/password from environment variables
2. **Screener.in Setup**: After authentication, users configure their Screener.in credentials
3. **Workflow Automation**: Users can then use the stock screening automation features

### Modifying Prompts

To change any prompts or messages, edit `prompts.py`:

```python
# Example: Modify the step breakdown prompt
STEP_BREAKDOWN_PROMPT = """
You are a screener automation agent specialized in stock market analysis and financial data extraction. 
Given the following user request, break it down into 3-8 clear, actionable steps that a browser automation agent can follow.
Each step should be specific and executable for stock screening tasks.

User Request: {user_request}

# Your custom prompt here...
"""
```

### Modifying Configuration

To change app settings, edit `config.py`:

```python
# Example: Change LLM model
LLM_MODEL = "gpt-4o-mini"  # Change to different model

# Example: Change browser settings
BROWSER_HEADLESS = True  # Run browser in headless mode
```

## 🔄 Migration from Monolithic to Modular

The original `main.py` file has been broken down into:

| Original Section | New File | Purpose |
|------------------|----------|---------|
| LLM prompts | `prompts.py` | Centralized prompt management |
| Configuration constants | `config.py` | App settings and constants |
| Agent functions | `agent_manager.py` | Browser automation logic |
| UI components | `ui_components.py` | Streamlit interface |
| Session state | `session_manager.py` | State management |
| Main logic | `main_new.py` | Application orchestration |

## 🎯 Benefits of Modular Structure

1. **Easy Prompt Modification**: All prompts in one file
2. **Centralized Configuration**: All settings in one place
3. **Better Maintainability**: Smaller, focused files
4. **Easier Testing**: Individual components can be tested
5. **Cleaner Code**: Separation of concerns
6. **Reusability**: Components can be reused in other projects

## 🔧 Customization Guide

### Adding New Prompts
1. Add new prompt variables to `prompts.py`
2. Import them in the relevant module
3. Use them in your code

### Adding New Configuration
1. Add new constants to `config.py`
2. Import them where needed
3. Use them in your components

### Adding New UI Components
1. Add new methods to `UIComponents` class in `ui_components.py`
2. Call them from `main_new.py`

### Adding New Agent Features
1. Add new methods to `AgentManager` class in `agent_manager.py`
2. Call them from UI components as needed

## 🐛 Troubleshooting

### Import Errors
- Ensure all files are in the same directory
- Check that all required packages are installed
- Verify file names match import statements

### Session State Issues
- Use `SessionManager` methods for state operations
- Initialize session state at app startup
- Reset state properly when needed

### Prompt Issues
- Check `prompts.py` for correct variable names
- Ensure proper string formatting
- Verify LLM model compatibility

## 📝 Notes

- The original `main.py` is kept for reference
- All functionality is preserved in the modular version
- The modular version is easier to maintain and extend
- Prompts can be easily modified without touching the main logic 