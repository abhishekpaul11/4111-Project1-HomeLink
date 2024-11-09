# streamlit_app/login.py
import time
from flask import json
import streamlit as st
from login import show_login
from dashboard import show_dashboard
from src.popo.User import User
from src.utils.browserUtils import get_local_storage, set_local_storage
from streamlit_local_storage import LocalStorage


localS = LocalStorage()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Login"

if not st.session_state['authenticated']:
    # check if user is saved in local storage


    user_json = localS.getItem("user")
    if user_json:
        user_data = json.loads(user_json)
        print(user_json)
        user = User(**user_data)
        st.session_state['user'] =user 
        st.session_state['current_page'] = "Dashboard"
        st.session_state['authenticated'] = True

def sidebar():
    if st.session_state['authenticated']:
        st.sidebar.title("Navigation")
        choice = st.sidebar.radio("Go to", ["Dashboard", "Logout"])
        
        if choice == "Dashboard":
            st.session_state['current_page'] = "Dashboard"
        elif choice == "Logout":
            st.session_state['authenticated'] = False
            st.session_state['current_page'] = "Login"
            st.session_state['username'] = None

            localS.deleteItem("user")
            time.sleep(0.5)
            st.rerun(scope="app")

# Display the correct page
def main():
    sidebar()
    
    if st.session_state['current_page'] == "Login":
        show_login()
    elif st.session_state['current_page'] == "Dashboard":
        show_dashboard()

# Run the main function
if __name__ == "__main__":
    main()