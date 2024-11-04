# streamlit_app/main.py
import streamlit as st
import requests

def show_dashboard():
    st.title("Dashboard")
    if st.session_state['just_logged_in']:
        st.success("Login successful!")
        st.session_state['just_logged_in'] = False
    st.text("Welcome " + st.session_state['username'])