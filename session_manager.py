# Session state management for the Workflow Automator

import streamlit as st
from config import SESSION_KEYS

class SessionManager:
    """Manages Streamlit session state initialization and operations."""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables with default values."""
        for key, default_value in SESSION_KEYS.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def reset_workflow_state():
        """Reset workflow-related session state."""
        workflow_keys = [
            'workflow_steps', 'workflow_approved', 'current_prompt',
            'show_workflow_view', 'editing_step', 'edited_steps',
            'agent_ran', 'latest_thoughts', 'agent_error', 'combined_prompt'
        ]
        
        for key in workflow_keys:
            if key in st.session_state:
                st.session_state[key] = SESSION_KEYS.get(key, None)
    
    @staticmethod
    def reset_agent_state():
        """Reset agent-related session state."""
        agent_keys = ['agent_ran', 'latest_thoughts', 'agent_error']
        
        for key in agent_keys:
            if key in st.session_state:
                st.session_state[key] = SESSION_KEYS.get(key, False)
    
    @staticmethod
    def reset_credentials():
        """Reset credentials-related session state."""
        credential_keys = ['credentials_configured', 'sensitive_data']
        
        for key in credential_keys:
            if key in st.session_state:
                st.session_state[key] = SESSION_KEYS.get(key, False)
    
    
    @staticmethod
    def get_session_info():
        """Get basic session state information for debugging."""
        return {
            'credentials_configured': st.session_state.get('credentials_configured', False),
            'workflow_steps_count': len(st.session_state.get('workflow_steps', [])),
            'workflow_approved': st.session_state.get('workflow_approved', False),
            'show_workflow_view': st.session_state.get('show_workflow_view', False),
            'agent_ran': st.session_state.get('agent_ran', False),
            'agent_error': st.session_state.get('agent_error', False),
            'editing_step': st.session_state.get('editing_step', None),
            'has_combined_prompt': bool(st.session_state.get('combined_prompt', ''))
        } 