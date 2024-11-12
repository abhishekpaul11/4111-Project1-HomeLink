# streamlit_app/main.py
from typing import List
from flask import json
import streamlit as st
from src.utils.reqs import sendDelReq, sendGetReq, sendPostReq
from src.popo.Apartment import Apartment

from src.popo.User import User

def delete_apartment(apt_id: int):
    response = sendDelReq("/owner/delete_apartment", {"apt_id": apt_id})
    if response.status_code == 200:
        st.success("Apartment deleted successfully!")
    else:
        st.error("Failed to delete apartment.")

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

@st.fragment
def show_owner_details():
    user:User = st.session_state['user']

    apartment_sqls:List = json.loads(sendGetReq("/owner/apt", {"user_id": user.user_id}).text)
    if len(apartment_sqls) == 0:
        st.text("You do not have any apartments yet")
    else:
        st.header("Your Apartments")
        for apt_sql in apartment_sqls:
            result:Apartment = Apartment(**apt_sql)
            result.owner_display(st)
            if st.button(f"Delete Apartment {result.apt_id}"):
                delete_apartment(result.apt_id)
                st.rerun(scope="show_owner_details")

@st.fragment
def show_broker_details():
    user:User = st.session_state['user']

    apartment_sqls:List = json.loads(sendGetReq("/broker/apt", {"user_id": user.user_id}).text)
    if len(apartment_sqls) == 0:
        st.text("You do not have any apartments yet")
    else:
        st.header("Your Apartments")
        for apt_sql in apartment_sqls:
            result:Apartment = Apartment(**apt_sql)
            result.owner_display(st)

@st.fragment
def create_apartment_owner():
    with st.form("apartment_form"):
        st.subheader("Add a New Apartment")
        apt_address = st.text_input("Address")
        apt_rent = st.number_input("Rent (in $)", min_value=0)
        apt_rooms = st.number_input("Rooms", min_value=1, step=1)
        suburb = st.text_input("Suburb")
        distance_frm_fin = st.number_input("Distance from Financial District (in kms)", min_value=0)
        apt_owner = st.text_input("Owner ID", value=st.session_state['user'].user_id, disabled=True)  # Default to the logged-in user
        apt_manager = st.text_input("Manager ID")

        # Add a submit button to the form
        submitted = st.form_submit_button("Create Apartment")

        if submitted:
            # Gather form data into a dictionary
            apartment_data = {
                "apt_address": apt_address,
                "apt_rent": apt_rent,
                "apt_rooms": apt_rooms,
                "suburb": suburb,
                "distance_frm_fin": distance_frm_fin,
                "apt_owner": apt_owner,
                "apt_manager": apt_manager if len(apt_manager)>0 else apt_owner,
            }

            # Send data to the backend
            response = sendPostReq("/owner/create_apartment", apartment_data)

            if response.status_code == 200:
                st.success("Apartment created successfully!")
            else:
                st.error("Failed to create apartment.")




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
    elif user_type == "Owner":
        create_apartment_owner()
        show_owner_details()
    elif user_type == "Broker":
        show_broker_details()