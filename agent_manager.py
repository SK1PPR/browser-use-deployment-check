import streamlit as st
from prompts import ERROR_BREAKDOWN, ERROR_COMBINE_STEPS, AGENT_TASK_PREFIX
from langchain_openai import ChatOpenAI
from config import LLM_MODEL

llm = ChatOpenAI(model=LLM_MODEL)

async def break_down_prompt(prompt):
    """Use LLM to break down user prompt into actionable steps."""
    from prompts import STEP_BREAKDOWN_PROMPT
    
    breakdown_prompt = STEP_BREAKDOWN_PROMPT.format(user_request=prompt)
    
    try:
        response = await llm.ainvoke(breakdown_prompt)
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

async def combine_steps_into_prompt(original_request, steps):
    """Use LLM to combine approved steps into a comprehensive prompt for browser automation."""
    from prompts import STEP_COMBINATION_PROMPT
    
    approved_steps = '\n'.join(f"{i+1}. {step}" for i, step in enumerate(steps))
    combine_prompt = STEP_COMBINATION_PROMPT.format(
        original_request=original_request,
        approved_steps=approved_steps
    )
    
    try:
        response = await llm.ainvoke(combine_prompt)
        return response.content.strip()
    except Exception as e:
        st.error(ERROR_COMBINE_STEPS.format(error=e))
        # Fallback: create a simple combined prompt
        fallback_prompt = AGENT_TASK_PREFIX.format(
            task=original_request, 
            steps='; '.join(steps)
        )
        return fallback_prompt
