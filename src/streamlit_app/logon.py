import streamlit as st
import requests
from enum import Enum

from src.utils.reqs import sendPostReq

def show_logon():
    # Streamlit logon page
    st.title("Logon Page")

    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    role = st.selectbox("Role", ["Tenant", "Owner", "Broker", "Repairmen"])
    broker_successful_deals = st.number_input("Broker Successful Deals", min_value=0, step=1)

    if st.button("Submit"):
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
            "broker_successful_deals": broker_successful_deals if role == "Broker" else None,
        }

        # Send data to the backend
        response = sendPostReq("/user/",{}, user_data)

        if response.status_code == 200:
            st.success("User created successfully!")
        else:
            st.error("Failed to create User.")