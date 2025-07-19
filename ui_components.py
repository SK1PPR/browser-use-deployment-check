# UI components for the Workflow Automator

import streamlit as st
import os
import asyncio
from prompts import *
from config import COLUMN_RATIOS, APP_TITLE

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
        
        # Show current email in sidebar
        if st.session_state['sensitive_data']:
            st.sidebar.info(f"Logged in as: {st.session_state['sensitive_data'].get('email', 'Unknown')}")

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
                        from agent_manager import AgentManager
                        agent_manager = AgentManager()
                        steps = asyncio.run(agent_manager.break_down_prompt(user_input))
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
                        from agent_manager import AgentManager
                        agent_manager = AgentManager()
                        combined_prompt = asyncio.run(agent_manager.combine_steps_into_prompt(
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
            
            if st.button(RESET_WORKFLOW):
                st.session_state['workflow_steps'] = []
                st.session_state['workflow_approved'] = False
                st.session_state['current_prompt'] = ""
                st.session_state['agent_ran'] = False
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
                st.info(f"Logged in as: {st.session_state['sensitive_data'].get('email', 'Unknown')}")
        
        # Show approved workflow info
        st.success(f"✅ **Approved Workflow:** {st.session_state['current_prompt']}")
        
        # Show the combined execution prompt
        if st.session_state.get('combined_prompt'):
            with st.expander(EXECUTION_PROMPT_TITLE, expanded=True):
                st.markdown("**Combined Prompt for Browser Agent:**")
                st.text_area("", value=st.session_state['combined_prompt'], height=150, disabled=True)
                st.info(EXECUTION_PROMPT_DESCRIPTION)
        
        # Debug information - minimal to avoid React errors
        if st.checkbox("🔧 Show Debug Info"):
            st.markdown(f"### {DEBUG_TITLE}")
            
            # Only show basic info to avoid session state issues
            st.markdown(f"**{DEBUG_ENVIRONMENT}**")
            st.markdown(f"- {DEBUG_WORKING_DIR.format(dir=os.getcwd())}")
            st.markdown(f"- {DEBUG_SCREENSHOTS_EXIST.format(exists=os.path.exists('screenshots'))}")
            
            # Simple browser test without complex state
            if st.button(DEBUG_BROWSER_TEST):
                st.info(DEBUG_BROWSER_TESTING)
                st.success("Browser test initiated!")
        
        # Execute workflow button
        if st.button(EXECUTE_WORKFLOW_BUTTON, type="primary", use_container_width=True):
            try:
                # Reset state
                st.session_state['agent_ran'] = False
                st.session_state['agent_error'] = False
                st.session_state['latest_thoughts'] = ''
                
                # Clear placeholders
                if 'thoughts_placeholder' in st.session_state:
                    st.session_state['thoughts_placeholder'].empty()
                if 'screenshot_placeholder' in st.session_state:
                    st.session_state['screenshot_placeholder'].empty()
                
                # Clean up screenshots
                from agent_manager import AgentManager
                agent_manager = AgentManager()
                agent_manager.cleanup_screenshots()
                
                # Show initial status
                st.info(WORKFLOW_STARTING)
                
                # Use the combined prompt for execution
                execution_prompt = st.session_state.get('combined_prompt', st.session_state['current_prompt'])
                
                # Run agent with timeout protection
                try:
                    asyncio.run(agent_manager.execute_workflow(
                        execution_prompt, 
                        st.session_state['thoughts_placeholder'], 
                        st.session_state['screenshot_placeholder']
                    ))
                except Exception as e:
                    st.error(ERROR_RUN_AGENT.format(error=e))
                    print(ERROR_RUN_AGENT.format(error=e))
                    st.session_state['agent_ran'] = False
                    st.session_state['agent_error'] = True
                    
            except Exception as e:
                st.error(ERROR_START_WORKFLOW.format(error=e))
                print(ERROR_START_WORKFLOW.format(error=e))
                st.session_state['agent_ran'] = False
                st.session_state['agent_error'] = True

        col1, col2 = st.columns(COLUMN_RATIOS['workflow'])

        # Left Column - Agent's Thoughts
        with col1:
            st.subheader(AGENT_THOUGHTS_HEADER)

            # Create a placeholder for live thoughts
            if 'thoughts_placeholder' not in st.session_state:
                st.session_state['thoughts_placeholder'] = st.empty()
            else:
                # Clear the placeholder if not running
                if not st.session_state.get('agent_ran', False):
                    st.session_state['thoughts_placeholder'].empty()
            
            # Static fallback below
            if st.session_state['latest_thoughts']:
                with st.expander("Agent's Thoughts (History)", expanded=True):
                    st.markdown(st.session_state['latest_thoughts'])
            else:
                st.info("Thoughts will appear here after agent runs.")

        # Right Column - Browser Screenshot
        with col2:
            st.subheader(BROWSER_SCREENSHOT_HEADER)
            # Screenshot will be shown live via the placeholder
            if 'screenshot_placeholder' not in st.session_state:
                st.session_state['screenshot_placeholder'] = st.empty()
            else:
                if not st.session_state.get('agent_ran', False):
                    st.session_state['screenshot_placeholder'].empty()
            st.session_state['screenshot_placeholder'].info("Run the agent to generate a screenshot.")

            # After agent completes, show a slider to browse all screenshots
            if st.session_state.get('agent_ran', False):
                screenshots_dir = 'screenshots'
                if os.path.exists(screenshots_dir):
                    screenshots = sorted([f for f in os.listdir(screenshots_dir) if f.startswith('step_') and f.endswith('.png')])
                    if screenshots:
                        step_numbers = [int(s.split('_')[1].split('.')[0]) for s in screenshots]
                        selected_step = st.slider("Select Step", min_value=min(step_numbers), max_value=max(step_numbers), value=max(step_numbers))
                        selected_screenshot = f'step_{selected_step}.png'
                        screenshot_path = os.path.join(screenshots_dir, selected_screenshot)
                        if os.path.exists(screenshot_path):
                            with open(screenshot_path, 'rb') as f:
                                img_bytes = f.read()
                            st.image(img_bytes, caption=f"Step {selected_step} Screenshot", use_container_width=True)
                        else:
                            st.warning(f"Screenshot for step {selected_step} not found.")
                    else:
                        st.info("No screenshots found.") 