import streamlit as st
from chat_db import init_db, save_message, load_history, clear_history, list_sessions
from fake_llm import get_fake_llm_response
from memory_utils import init_session
import uuid
 
st.set_page_config(page_title="Streamlit Chat with Multi-Session Memory", layout="wide")
st.title("Chat App with Multi-Session Memory & SQLite")
 
init_db()
init_session()
 
st.sidebar.header("🗂️Chat Sessions")
sessions = list_sessions()
 
if sessions:
    for sid, ts, preview in sessions:
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            label = f"{sid[:8]}... — {preview[:30] if preview else 'Empty'}"
            if st.button(label, key=f"load_{sid}"):
                st.session_state["session_id"] = sid
                st.session_state["messages"] = load_history(sid)
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_{sid}"):
                clear_history(sid)
                if st.session_state["session_id"] == sid:
                    st.session_state["session_id"] = str(uuid.uuid4())
                    st.session_state["messages"] = []
                st.rerun()
 
if st.sidebar.button("New Chat"):
    st.session_state["session_id"] = str(uuid.uuid4())
    st.session_state["messages"] = []
    st.rerun()
 
if st.sidebar.button("Clear Current Chat"):
    clear_history(st.session_state["session_id"])
    st.session_state["messages"] = []
    st.rerun()
 
# Load current session
session_id = st.session_state["session_id"]
messages = load_history(session_id)
st.session_state["messages"] = messages
 
st.sidebar.markdown(f"**Current Session:** `{session_id[:8]}...`")
 
# Chat Interface
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state["messages"].append(("User", user_input))
    save_message(session_id, "User", user_input)
 
    fake_llm = get_fake_llm_response(user_input, session_id)
    llm_response = fake_llm.invoke(user_input)
 
    st.session_state["messages"].append(("Bot", llm_response))
    save_message(session_id, "Bot", llm_response)
      
#Display conversation
for role, msg in st.session_state["messages"]:
    with st.chat_message("user" if role == "User" else "assistant"):
        st.markdown(msg)
