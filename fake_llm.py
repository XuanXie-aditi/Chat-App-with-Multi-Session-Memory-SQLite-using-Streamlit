import streamlit as st
from langchain_community.llms.fake import FakeListLLM
 
RESPONSES = [
    "Hello there!",
    "How can I help you today?",
    "Goodbye!"
]
 
def get_fake_llm_response(user_input: str, session_id: str):
    """
    Returns a cycling FakeListLLM per session.
    Each session starts from the first response.
    """
    key = f"fake_llm_{session_id}"
 
    if key not in st.session_state:
        st.session_state[key] = FakeListLLM(responses=RESPONSES)
        
    return st.session_state[key]
