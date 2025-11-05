import streamlit as st
from chat_db import load_history
import uuid

def init_session():
    """
    Initialize Streamlit session state for chat messages.
    Loads previous chat history from the database if not already in session.
    """

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
        st.session_state["messages"] = []
    else:
        if not st.session_state["messages"]:
            st.session_state["messages"] = load_history(st.session_state["session_id"])
