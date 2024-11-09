# streamlit_app/main.py
from flask import json
import streamlit as st
from src.utils.reqs import sendGetReq
from src.popo.Apartment import Apartment

from src.popo.User import User

def show_tenant_details():
    user:User = st.session_state['user']
    
    apartment_sql = sendGetReq("tenants/apt", {"user_id": user.user_id}).text
    if apartment_sql == "":
        st.text("You do not have an apartment yet")
    else:
        result:Apartment = Apartment(**json.loads(apartment_sql))
        st.subheader("Your Apartment Details")
        st.text(f"Apartment ID: {result.apt_id}")
        st.text(f"Address: {result.apt_address}")
        st.text(f"Rent: {result.apt_rent}")
        st.text(f"Rooms: {result.apt_rooms}")
        st.text(f"Suburb: {result.suburb}")
        st.text(f"Distance from Financial District: {result.distance_frm_fin}")
        st.text(f"Owner ID: {result.apt_owner}")
        st.text(f"Manager ID: {result.apt_manager}")
        st.text(f"Tenant ID: {result.apt_tenant}")
        st.text(f"Rented Date: {result.apt_rented_date}")
        st.text(f"Rented Duration: {result.apt_rented_duration} months")


    



def show_dashboard():
    user:User = st.session_state['user']
    user_type = user.get_user_type()
    st.title(f"{user_type} Dashboard")
    if ('just_logged_in' in st.session_state) and st.session_state['just_logged_in']:
        st.success("Login successful!")
        st.session_state['just_logged_in'] = False
    st.text("Welcome " + user.name)
    if user_type == "Tenant":
        show_tenant_details()