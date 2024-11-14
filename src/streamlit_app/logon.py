import time

import streamlit as st
from flask import json
from streamlit_local_storage import LocalStorage

from src.popo.User import User
from src.utils.reqs import sendPostReq


def show_logon():
    # Streamlit logon page
    st.title("Sign-up on HomeLink")

    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    role = st.selectbox("How would you like to use our services? Select the role that best describes you.", ["Tenant", "Owner", "Broker", "Repairmen"])

    if st.button("Create Account"):
        if len(name) == 0 or len(password) == 0 or len(email) == 0 or len(phone) == 0:
            st.error("Please fill in all fields.")
            return
        user_data = {
            "name": name,
            "password": password,
            "email": email,
            "phone": phone,
            "is_owner": "TRUE" if role == "Owner" else "FALSE",
            "is_broker": "TRUE" if role == "Broker" else "FALSE",
            "is_tenant": "TRUE" if role == "Tenant" else "FALSE",
            "is_repairmen": "TRUE" if role == "Repairmen" else "FALSE",
            "broker_successful_deals": 0 if role == "Broker" else None,
        }

        # Send data to the backend
        response = sendPostReq("/user/",{}, user_data)

        if response.status_code == 200:
            st.success("Account created successfully!")
            st.session_state['authenticated'] = True
            st.session_state['current_page'] = "Dashboard"
            st.session_state['just_logged_in'] = True

            user_data = response.json()["user"]
            user = User(**user_data)
            st.session_state['user'] = user

            local_s = LocalStorage()
            local_s.setItem("user", json.dumps(user.get_user_dict()))
            time.sleep(0.5)

            st.rerun(scope="app")
        else:
            st.error("Failed to create account. Email or phone already exists.")

    st.write("")
    st.write("")

    if st.button("Go Back"):
        st.session_state['current_page'] = 'Login'
        st.rerun()