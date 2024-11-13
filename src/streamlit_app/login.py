# streamlit_app/login.py
import time
from typing import Tuple
from flask import json
import streamlit as st
from src.popo.User import User
from src.utils.reqs import sendGetReq
from src.utils.browserUtils import get_local_storage, set_local_storage
from streamlit_local_storage import LocalStorage

def check_login(username, password) -> bool:
    response = sendGetReq("auth", {"username": username, "password": password})

    # Print the response
    if response.status_code == 200:
        data = json.loads(response.text)  # Convert JSON string to a dictionary

        # Extract the `user` field and convert it to the `User` dataclass
        user_data = json.loads(data["user"])  # Convert `user` JSON string to a dictionary if it's stringified
        user = User(**user_data)
        return (True, user)
    elif response.status_code == 401:
        return (False, None)
    return (False, None)

def show_login():
    st.title("HomeLink")
    st.subheader("The Modern Housing Rental Marketplace !!!")

    st.write("")
    st.write("")

    st.header("Login")
    
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        (success, user) = check_login(username, password)
        if success:
            st.session_state['authenticated'] = True
            st.session_state['user'] =user 
            st.session_state['current_page'] = "Dashboard"
            st.session_state['just_logged_in'] = True

            localS = LocalStorage()
            localS.setItem("user", json.dumps(user.get_user_dict()))
            # local cache takes time to update
            time.sleep(0.5)

            st.rerun(scope="app")
        else:
            st.error("Invalid username or password")

    st.write("")
    st.write("")

    if st.button("Sign Up"):
        st.session_state['current_page'] = "logon"
        st.rerun(scope="app")