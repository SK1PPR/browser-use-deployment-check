# UI components for the Workflow Automator

import streamlit as st
import os
import asyncio
import time
from prompts import *
from config import COLUMN_RATIOS, APP_TITLE, get_env_var
from browser import execute_workflow, cleanup_screenshots

class UIComponents:
    """Manages all UI components and layouts."""
    
    @staticmethod
    def setup_page():
        """Setup the main page configuration."""
        st.set_page_config(
            page_title=APP_TITLE,
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    @staticmethod
    def authenticate_user():
        """Display the user authentication form."""
        st.title(LOGIN_WELCOME)
        st.markdown(LOGIN_INSTRUCTIONS)
        
        # Get environment variables for authentication
        env_username = get_env_var('APP_USERNAME')
        env_password = get_env_var('APP_PASSWORD')
        
        if not env_username or not env_password:
            st.error("Authentication not configured. Please set APP_USERNAME and APP_PASSWORD environment variables.")
            return
        
        with st.form("login_form"):
            st.subheader(LOGIN_HEADER)
            
            username = st.text_input(
                LOGIN_USERNAME_LABEL, 
                type="default", 
                help=LOGIN_USERNAME_HELP
            )
            password = st.text_input(
                LOGIN_PASSWORD_LABEL, 
                type="password", 
                help=LOGIN_PASSWORD_HELP
            )
            
            submitted = st.form_submit_button(LOGIN_BUTTON)
            
            if submitted:
                if username == env_username and password == env_password:
                    st.session_state['authenticated'] = True
                    st.session_state['login_error'] = ""
                    st.success(LOGIN_SUCCESS)
                    st.rerun()
                else:
                    st.session_state['login_error'] = LOGIN_ERROR
                    st.error(LOGIN_ERROR)
        
        # Show error message if login failed
        if st.session_state.get('login_error'):
            st.error(st.session_state['login_error'])
    
    @staticmethod
    def credentials_setup():
        """Display the credentials setup form."""
        st.title(CREDENTIALS_WELCOME)
        st.markdown(CREDENTIALS_INSTRUCTIONS)
        
        with st.form("credentials_form"):
            st.subheader(CREDENTIALS_HEADER)
            
            email = st.text_input(
                CREDENTIALS_EMAIL_LABEL, 
                type="default", 
                help=CREDENTIALS_EMAIL_HELP
            )
            password = st.text_input(
                CREDENTIALS_PASSWORD_LABEL, 
                type="password", 
                help=CREDENTIALS_PASSWORD_HELP
            )
            
            submitted = st.form_submit_button(CREDENTIALS_SAVE_BUTTON)
            
            if submitted:
                if email and password:
                    st.session_state['sensitive_data'] = {
                        'email': email,
                        'password': password
                    }
                    st.session_state['credentials_configured'] = True
                    st.success(CREDENTIALS_SUCCESS)
                    st.rerun()
                else:
                    st.error(CREDENTIALS_ERROR)
    
    @staticmethod
    def initial_input_view():
        """Display the initial input view."""
        st.title(WORKFLOW_TITLE)
        
        # Sidebar controls
        if st.sidebar.button(RECONFIGURE_CREDENTIALS):
            st.session_state['credentials_configured'] = False
            st.session_state['sensitive_data'] = {}
            st.rerun()
        
        if st.sidebar.button(LOGOUT_BUTTON):
            st.session_state['authenticated'] = False
            st.session_state['credentials_configured'] = False
            st.session_state['sensitive_data'] = {}
            st.session_state['login_error'] = ""
            st.rerun()
        
        # Show current email in sidebar
        if st.session_state['sensitive_data']:
            st.sidebar.info(f"Screener.in: {st.session_state['sensitive_data'].get('email', 'Unknown')}")

        # Centered input section
        col1, col2, col3 = st.columns(COLUMN_RATIOS['main'])
        
        with col2:
            st.markdown(f"### {START_WORKFLOW_HEADER}")
            st.markdown(START_WORKFLOW_DESCRIPTION)
            
            user_input = st.text_input(
                "Enter your workflow prompt:", 
                placeholder=WORKFLOW_INPUT_PLACEHOLDER
            )
            
            if st.button(BREAK_DOWN_BUTTON, type="primary", use_container_width=True):
                if user_input.strip():
                    st.session_state['current_prompt'] = user_input
                    st.session_state['workflow_approved'] = False
                    st.session_state['agent_ran'] = False
                    
                    with st.spinner("Breaking down your request into steps..."):
                        from agent_manager import break_down_prompt
                        steps = asyncio.run(break_down_prompt(user_input))
                        st.session_state['workflow_steps'] = steps
                    st.rerun()
                else:
                    st.error("Please enter a workflow prompt.")
    
    @staticmethod
    def step_breakdown_view():
        """Display the step breakdown view."""
        st.title(STEP_BREAKDOWN_TITLE)
        
        # Original request
        st.markdown(f"**🎯 Original Request:** {st.session_state['current_prompt']}")
        
        # Steps breakdown
        st.markdown(f"### {PROPOSED_STEPS_HEADER}")
        
        # Initialize edited_steps if not already done
        if not st.session_state['edited_steps']:
            st.session_state['edited_steps'] = st.session_state['workflow_steps'].copy()
        
        for i, step in enumerate(st.session_state['edited_steps'], 1):
            # Create a row for each step with number, text, and action buttons
            col_num, col_text, col_edit, col_delete = st.columns(COLUMN_RATIOS['step_actions'])
            
            with col_num:
                st.markdown(f"""
                <div style="background: #667eea; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: 0 auto;">
                    {i}
                </div>
                """, unsafe_allow_html=True)
            
            with col_text:
                st.markdown(f'<div style="color: #e0e0e0; padding: 0.5rem 0;">{step}</div>', unsafe_allow_html=True)
            
            with col_edit:
                if st.button("✏️", key=f"edit_{i}", help=f"Edit step {i}"):
                    st.session_state['editing_step'] = i - 1
                    st.rerun()
            
            with col_delete:
                if st.button("🗑️", key=f"delete_{i}", help=f"Delete step {i}"):
                    # If we're editing this step, stop editing
                    if st.session_state.get('editing_step') == i - 1:
                        st.session_state['editing_step'] = None
                    
                    # Remove the step
                    st.session_state['edited_steps'].pop(i - 1)
                    
                    # Adjust editing index if we deleted a step before the one being edited
                    if st.session_state.get('editing_step') is not None and st.session_state['editing_step'] > i - 1:
                        st.session_state['editing_step'] -= 1
                    
                    st.rerun()
            
            # Add separator line between steps
            if i < len(st.session_state['edited_steps']):
                st.markdown("---")
        
        # Add new step button
        if st.button(ADD_NEW_STEP, key="add_step"):
            st.session_state['edited_steps'].append("New step")
            st.rerun()
        
        # Edit step functionality
        if st.session_state['editing_step'] is not None:
            step_index = st.session_state['editing_step']
            
            # Validate that the step_index is still valid
            if step_index >= len(st.session_state['edited_steps']):
                st.error("Step no longer exists. Please refresh the page.")
                st.session_state['editing_step'] = None
                st.rerun()
            else:
                st.markdown(f"### {EDIT_STEP_TITLE}")
                
                edited_text = st.text_area(
                    "Step Description:",
                    value=st.session_state['edited_steps'][step_index],
                    key=f"edit_text_{step_index}",
                    height=100
                )
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(SAVE_BUTTON, key=f"save_{step_index}"):
                        st.session_state['edited_steps'][step_index] = edited_text
                        st.session_state['editing_step'] = None
                        st.rerun()
                
                with col_cancel:
                    if st.button(CANCEL_BUTTON, key=f"cancel_{step_index}"):
                        st.session_state['editing_step'] = None
                        st.rerun()
        
        # Approval buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(COLUMN_RATIOS['approval'])
        
        with col2:
            col_approve, col_reject = st.columns(2)
            
            with col_approve:
                if st.button(APPROVE_RUN_BUTTON, type="primary", use_container_width=True):
                    # Combine steps into a comprehensive prompt
                    with st.spinner("Combining steps into execution prompt..."):
                        from agent_manager import combine_steps_into_prompt
                        combined_prompt = asyncio.run(combine_steps_into_prompt(
                            st.session_state['current_prompt'], 
                            st.session_state['edited_steps']
                        ))
                        st.session_state['combined_prompt'] = combined_prompt
                    
                    st.session_state['workflow_approved'] = True
                    st.session_state['show_workflow_view'] = True
                    # Use edited steps for the workflow
                    st.session_state['workflow_steps'] = st.session_state['edited_steps'].copy()
                    st.rerun()
            
            with col_reject:
                if st.button(REJECT_MODIFY_BUTTON, use_container_width=True):
                    st.session_state['workflow_steps'] = []
                    st.session_state['workflow_approved'] = False
                    st.session_state['show_workflow_view'] = False
                    st.rerun()
        
        # Sidebar controls
        with st.sidebar:
            st.markdown("### 🎛️ Controls")
            
            if st.button(BACK_TO_INPUT):
                st.session_state['workflow_steps'] = []
                st.session_state['workflow_approved'] = False
                st.session_state['show_workflow_view'] = False
                st.session_state['edited_steps'] = []
                st.session_state['editing_step'] = None
                st.rerun()
    
    @staticmethod
    def workflow_execution_view():
        """Display the workflow execution view."""
        # Add error recovery
        if st.session_state.get('agent_error'):
            st.error("Previous agent execution failed. Please try again or check the debug info.")
            if st.button(RESET_ERROR_STATE):
                st.session_state['agent_error'] = False
                st.rerun()
        
        st.title(WORKFLOW_TITLE)
        
        # Sidebar controls
        with st.sidebar:
            st.markdown("### 🎛️ Controls")
            
            if st.button(RECONFIGURE_CREDENTIALS):
                st.session_state['credentials_configured'] = False
                st.session_state['sensitive_data'] = {}
                st.rerun()
            
            if st.button(LOGOUT_BUTTON):
                st.session_state['authenticated'] = False
                st.session_state['credentials_configured'] = False
                st.session_state['sensitive_data'] = {}
                st.session_state['login_error'] = ""
                st.rerun()
            
            if st.button(RESET_WORKFLOW):
                st.session_state['workflow_steps'] = []
                st.session_state['workflow_approved'] = False
                st.session_state['current_prompt'] = ""
                st.session_state['agent_ran'] = False
                st.session_state['agent_completed'] = False
                st.session_state['final_result'] = ""
                st.session_state['start_realtime_updates'] = False
                st.session_state['latest_thoughts'] = ""
                st.session_state['show_workflow_view'] = False
                st.session_state['edited_steps'] = []
                st.session_state['editing_step'] = None
                st.rerun()
            
            if st.button(BACK_TO_STEP_BREAKDOWN):
                st.session_state['show_workflow_view'] = False
                st.rerun()
            
            # Show current email in sidebar
            if st.session_state['sensitive_data']:
                st.info(f"Screener.in: {st.session_state['sensitive_data'].get('email', 'Unknown')}")
        
        # Show approved workflow info
        st.success(f"✅ **Approved Workflow:** {st.session_state['current_prompt']}")
        
        # Show the combined execution prompt
        if st.session_state.get('combined_prompt'):
            with st.expander(EXECUTION_PROMPT_TITLE, expanded=False):
                st.markdown("**Combined Prompt for Browser Agent:**")
                st.text_area("", value=st.session_state['combined_prompt'], height=150, disabled=True)
                st.info(EXECUTION_PROMPT_DESCRIPTION)
        
            # Execute workflow button
            if st.button(EXECUTE_WORKFLOW_BUTTON, type="primary", use_container_width=True):
                # Reset state for new run
                st.session_state['agent_ran'] = False
                st.session_state['agent_completed'] = False
                st.session_state['final_result'] = ""
                st.session_state['start_realtime_updates'] = False
                st.session_state['agent_error'] = False
                st.session_state['latest_thoughts'] = ''
                st.session_state['step_counter'] = {'n': 0}
                
                # Clean up screenshots
                cleanup_screenshots()
                
                # Set flag to start real-time updates
                st.session_state['start_realtime_updates'] = True
                
                # Use the combined prompt for execution
                execution_prompt = st.session_state.get('combined_prompt', st.session_state['current_prompt'])
                
                # Run agent with timeout protection
                asyncio.run(execute_workflow(execution_prompt))

        # Real-time update logic - use auto-rerun when agent is running
        if st.session_state.get('agent_ran', False) and not st.session_state.get('agent_completed', False):
            # Auto-rerun every 2 seconds to show live updates
            time.sleep(2)
            st.rerun()

        col1, col2 = st.columns(COLUMN_RATIOS['workflow'])

        # Left Column - Agent's Thoughts
        with col1:
            st.subheader(AGENT_THOUGHTS_HEADER)

            # Show thoughts with live updates
            if st.session_state['latest_thoughts']:
                with st.expander("Agent's Live Actions", expanded=True):
                    st.markdown(st.session_state['latest_thoughts'])
                    
                    # Show current status only when agent is running and not completed
                    if st.session_state.get('agent_ran', False) and not st.session_state.get('agent_completed', False):
                        current_step = st.session_state.get('step_counter', {}).get('n', 0)
                        screenshots_count = len(st.session_state.get('screenshots', []))
                        
                        # Show progress bar
                        if current_step > 0:
                            progress_text = f"🔄 Agent is currently running... (Step {current_step}, Screenshots: {screenshots_count})"
                            st.success(progress_text)
                            
                            # Show a simple progress indicator
                            progress = min(current_step / max(current_step, 1), 1.0)
                            st.progress(progress, text=f"Progress: Step {current_step}")
                        else:
                            st.info("🔄 Agent is starting... Actions will appear here as they happen.")
            else:
                if st.session_state.get('agent_ran', False) and not st.session_state.get('agent_completed', False):
                    st.info("🔄 Agent is starting... Actions will appear here as they happen.")
                    st.progress(0, text="Initializing agent...")
                else:
                    st.info("Agent actions will appear here as they happen.")

        # Right Column - Browser Screenshot
        with col2:
            st.subheader(BROWSER_SCREENSHOT_HEADER)
            
            # Show screenshots in real-time as they're captured
            screenshots = st.session_state.get('screenshots', [])
            if screenshots:    
                # If there are multiple screenshots, show a slider below to browse them
                if len(screenshots) > 1:
                    st.markdown("**Browse Steps:**")
                    step_numbers = list(range(1, len(screenshots) + 1))
                    selected_step = st.slider("Select Step", min_value=1, max_value=len(screenshots), value=len(screenshots))
                    if selected_step != len(screenshots):  # Don't show the same image twice
                        selected_screenshot = screenshots[selected_step - 1]
                        st.image(selected_screenshot, caption=f"Step {selected_step} Screenshot", use_container_width=True)
            else:
                if st.session_state.get('agent_ran', False) and not st.session_state.get('agent_completed', False):
                    st.info("Agent is running... Screenshots will appear here as steps are completed.")
                    # Show a spinner to indicate activity
                    with st.spinner("Capturing screenshots..."):
                        st.empty()
                else:
                    st.info("Run the agent to generate screenshots.")
        
        # Final Results Section - Show at bottom when agent completes
        if st.session_state.get('agent_completed', False) and st.session_state.get('final_result'):
            st.markdown("---")
            st.subheader(FINAL_RESULTS_TITLE)
            
            # Display the final result
            final_result = st.session_state.get('final_result', "")
            if final_result:
                with st.expander(VIEW_FINAL_RESULTS, expanded=True):
                    st.markdown(f"**{FINAL_RESULTS_HEADER}:**")
                    st.write(final_result)