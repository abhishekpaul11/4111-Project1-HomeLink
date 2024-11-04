# streamlit_app/login.py
import streamlit as st
from src.utils.reqs import sendGetReq

def check_login(username, password) -> bool:
    response = sendGetReq("auth", {"username": username, "password": password})

    # Print the response
    if response.status_code == 200:
        return True
    elif response.status_code == 401:
        return False
    return False

def show_login():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_login(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.session_state['current_page'] = "Dashboard"
            st.session_state['just_logged_in'] = True
            st.rerun(scope="app")
        else:
            st.error("Invalid username or password")