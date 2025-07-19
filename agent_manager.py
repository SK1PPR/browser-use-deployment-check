# Agent management for browser automation

import asyncio
import base64
import os
import shutil
import traceback
from langchain_openai import ChatOpenAI
from browser_use import Agent
import streamlit as st
from config import LLM_MODEL, LLM_TEMPERATURE, BROWSER_CONFIG, INITIAL_ACTIONS
from prompts import (
    ERROR_CREATE_AGENT, ERROR_AGENT_EXECUTION, ERROR_CRITICAL,
    AGENT_RUNNING, AGENT_COMPLETED, AGENT_FAILED, BROWSER_KEEP_OPEN,
    ERROR_BREAKDOWN, ERROR_COMBINE_STEPS, AGENT_TASK_PREFIX
)

class AgentManager:
    """Manages browser automation agent operations."""
    
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    
    async def break_down_prompt(self, prompt):
        """Use LLM to break down user prompt into actionable steps."""
        from prompts import STEP_BREAKDOWN_PROMPT
        
        breakdown_prompt = STEP_BREAKDOWN_PROMPT.format(user_request=prompt)
        
        try:
            response = await self.llm.ainvoke(breakdown_prompt)
            steps_text = response.content
            steps = []
            
            for line in steps_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('•') or line.startswith('-') or line.startswith('*')):
                    step = line
                    if '. ' in line:
                        step = line.split('. ', 1)[1]
                    elif ') ' in line:
                        step = line.split(') ', 1)[1]
                    elif ' ' in line and line[0].isdigit():
                        step = line.split(' ', 1)[1]
                    elif line.startswith(('•', '-', '*')):
                        step = line[1:].strip()
                    
                    if step:
                        steps.append(step)
            
            return steps if steps else ["1. " + steps_text]
        except Exception as e:
            st.error(ERROR_BREAKDOWN.format(error=e))
            return [f"1. Execute the following task: {prompt}"]
    
    async def combine_steps_into_prompt(self, original_request, steps):
        """Use LLM to combine approved steps into a comprehensive prompt for browser automation."""
        from prompts import STEP_COMBINATION_PROMPT
        
        approved_steps = '\n'.join(f"{i+1}. {step}" for i, step in enumerate(steps))
        combine_prompt = STEP_COMBINATION_PROMPT.format(
            original_request=original_request,
            approved_steps=approved_steps
        )
        
        try:
            response = await self.llm.ainvoke(combine_prompt)
            return response.content.strip()
        except Exception as e:
            st.error(ERROR_COMBINE_STEPS.format(error=e))
            # Fallback: create a simple combined prompt
            fallback_prompt = AGENT_TASK_PREFIX.format(
                task=original_request, 
                steps='; '.join(steps)
            )
            return fallback_prompt
    
    async def execute_workflow(self, query, thoughts_placeholder, screenshot_placeholder):
        """Execute the workflow using the browser automation agent."""
        try:
            # Use the session state step counter
            step_counter = st.session_state['step_counter']

            # Create agent with simplified configuration
            try:
                agent = Agent(
                    task=query,
                    llm=self.llm,
                    temperature=LLM_TEMPERATURE,
                    headless=False,
                    keep_alive=True,
                    browser_config=BROWSER_CONFIG
                )
            except Exception as e:
                st.error(ERROR_CREATE_AGENT.format(error=e))
                print(ERROR_CREATE_AGENT.format(error=e))
                return

            # Run agent with simple approach
            try:
                print(f"\n🚀 Running the task: {query}\n")
                
                # Update UI before starting
                with thoughts_placeholder.expander("Agent Status", expanded=True):
                    st.markdown(f"**{AGENT_RUNNING}**")
                    st.markdown(f"**Task:** {query}")
                
                # Simple agent run without complex callbacks
                result = await agent.run()
                
                # Update session state first
                st.session_state['agent_ran'] = True
                st.session_state['agent_error'] = False
                
                # Update UI after completion
                with thoughts_placeholder.expander("Agent Status", expanded=True):
                    st.markdown(f"**{AGENT_COMPLETED}**")
                    st.markdown(f"**Task:** {query}")
                
                # Show extracted content if available
                if hasattr(result, 'extracted_content') and result.extracted_content():
                    with thoughts_placeholder.expander("Extracted Content", expanded=True):
                        st.markdown(result.extracted_content())
                
                # Keep browser open for user review
                if hasattr(agent, 'browser_session') and agent.browser_session:
                    st.info(BROWSER_KEEP_OPEN)
                    
            except Exception as e:
                st.error(ERROR_AGENT_EXECUTION.format(error=e))
                print(ERROR_AGENT_EXECUTION.format(error=e))
                traceback.print_exc()
                st.session_state['agent_ran'] = False
                st.session_state['agent_error'] = True
                
                # Update UI with error
                with thoughts_placeholder.expander("Agent Status", expanded=True):
                    st.markdown(f"**{AGENT_FAILED}**")
                    st.markdown(f"**Error:** {str(e)}")
                return

        except Exception as e:
            st.error(ERROR_CRITICAL.format(error=e))
            print(ERROR_CRITICAL.format(error=e))
            traceback.print_exc()
            st.session_state['agent_ran'] = False
    
    def cleanup_screenshots(self):
        """Clean up screenshots directory and reset step counter."""
        screenshots_dir = 'screenshots'
        if os.path.exists(screenshots_dir):
            shutil.rmtree(screenshots_dir)
        os.makedirs(screenshots_dir, exist_ok=True)
        st.session_state['step_counter'] = {'n': 0} 