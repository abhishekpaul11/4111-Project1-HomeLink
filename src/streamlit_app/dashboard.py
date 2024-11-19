# streamlit_app/main.py
import datetime
from typing import List
from flask import json
import streamlit as st
from src.streamlit_app.formatting.apartments import display_apartment
from src.streamlit_app.formatting.apartments_broker import display_apartment_for_broker
from src.streamlit_app.formatting.apartments_tenant import display_apartment_for_tenant
from src.streamlit_app.formatting.appointments import display_appointment
from src.streamlit_app.formatting.appointments_repairmen import display_appointment_for_repairmen
from src.streamlit_app.formatting.issues import display_issue
from src.streamlit_app.formatting.issues_repairmen import display_issue_for_repairmen
from src.utils.reqs import sendDelReq, sendGetReq, sendPostReq

from src.popo.User import User, UserType

def delete_apartment(apt_id: int):
    response = sendDelReq("/owner/delete_apartment", {"apt_id": apt_id})
    if response.status_code == 200:
        st.success("Apartment deleted successfully!")
    else:
        st.error("Failed to delete apartment.")

def show_tenant_details():
    user:User = st.session_state['user']

    st.header("My Apartment Details")
    apartment_sql = sendGetReq("tenants/apt", {"user_id": user.user_id}).text
    if apartment_sql == "":
        st.session_state['is_lease_on'] = False
        st.text("You do not have an apartment yet")
    else:
        st.session_state['is_lease_on'] = True
        apartment_sql = json.loads(apartment_sql)
        display_apartment_for_tenant(apartment_sql)
        st.write("")
        st.write("")

        st.header("Reported Issues")
        issues_display(apartment_sql['apt_id'])
        st.write("")
        st.write("")

        st.header("Active Appointments")
        scheduled_appointments(apartment_sql['apt_id'])
        st.write("")
        st.write("")

        st.header("Create An Issue")
        show_issue_form(apartment_sql['apt_id'])

@st.fragment
def show_owner_details():
    user:User = st.session_state['user']

    st.header("My Apartments")
    apartment_sqls:List = json.loads(sendGetReq("/owner/apt", {"user_id": user.user_id}).text)
    if len(apartment_sqls) == 0:
        st.text("You do not have any apartments yet")
    else:
        for apt_sql in apartment_sqls:
            display_apartment(apt_sql)
            if st.button(f"Delete Apartment {apt_sql['apt_id']}"):
                delete_apartment(apt_sql['apt_id'])
                st.rerun(scope="show_owner_details")

@st.fragment
def show_broker_details():
    user:User = st.session_state['user']

    apartment_sqls:List = json.loads(sendGetReq("/broker/apt", {"user_id": user.user_id}).text)
    if len(apartment_sqls) == 0:
        st.text("You do not have any apartments yet")
    else:
        st.header("My Managed Apartments")
        for apt_sql in apartment_sqls:
            display_apartment_for_broker(apt_sql)

@st.fragment
def create_apartment_owner():
    with st.form("apartment_form"):

        brokers = json.loads(sendGetReq('owner/get_brokers').text)

        st.subheader("Add a New Apartment")
        apt_address = st.text_input("Address")
        apt_rent = st.number_input("Rent (in $)", min_value=1)
        apt_rooms = st.number_input("Rooms", min_value=1, step=1)
        suburb = st.text_input("Suburb")
        distance_frm_fin = st.number_input("Distance from Financial District (in kms)", min_value=0)

        broker_options = ['Choose a Broker']
        if len(brokers) > 0: broker_options.append('I\'ll manage it myself')

        for broker in brokers:
            broker_options.append(f'{broker['user_id']}. {broker["name"]}: {broker["broker_successful_deals"]} past deals closed')

        if len(broker_options) > 1:
            selected_option = st.selectbox("Choose a broker to manage this property on your behalf", broker_options)

        submitted = st.form_submit_button("Create Apartment")

        if submitted:
            if len(apt_address) == 0 or len(suburb) == 0 or (len(broker_options) > 1 and selected_option == 'Choose a Broker'):
                st.error("Please fill in all fields.")
                return

            if len(broker_options) > 1:
                if selected_option == 'I\'ll manage it myself':
                    apt_broker_id = st.session_state['user'].user_id
                else:
                    apt_broker_id = selected_option.split('.')[0]
            else:
                apt_broker_id = st.session_state['user'].user_id

            # Gather form data into a dictionary
            apartment_data = {
                "apt_address": apt_address,
                "apt_rent": apt_rent,
                "apt_rooms": apt_rooms,
                "suburb": suburb,
                "distance_frm_fin": distance_frm_fin,
                "apt_owner": st.session_state['user'].user_id,
                "apt_manager": apt_broker_id,
            }

            # Send data to the backend
            response = sendPostReq("/owner/create_apartment", apartment_data)

            if response.status_code == 200:
                st.success("Apartment created successfully!")
                st.rerun()
            else:
                st.error("Failed to create apartment.")


def show_issue_form(apt_id:int):
    with st.form("issue_form"):
        st.subheader("Issue Description")
        issue = st.text_area(label="desc", label_visibility='hidden')

        # Add a submit button to the form
        submitted = st.form_submit_button("Report Issue")

        if submitted:

            if len(issue) == 0:
                st.error("Please enter a description.")
                return

            # Gather form data into a dictionary
            issue_data = {
                "apt_id": apt_id,
                "issue": issue,
                "issue_date": datetime.date.today().isoformat(),
            }

            # Send data to the backend
            response = sendPostReq("/tenant/report_issue",{}, issue_data)

            if response.status_code == 200:
                st.success("Issue reported successfully!")
                st.rerun()
            else:
                st.error("Failed to report issue.")

def issues_display(apt_id:int):
    issues:List = json.loads(sendGetReq("/tenant/issues", {"apt_id": apt_id}).text)
    if len(issues) == 0:
        st.text("No issues reported yet")
    else:
        for issue in issues:
            display_issue(issue)

def scheduled_appointments(apt_id:int):
    appointments: List = json.loads(sendGetReq("/tenant/appointments", {"apt_id": apt_id}).text)
    if len(appointments) == 0:
        st.text("No appointments scheduled yet")
    else:
        for appointment in appointments:
            display_appointment(appointment)
            if st.button(f"Resolve", key = str(appointment['appointment_id'])+"_resolve"):
                response = sendDelReq("/tenant/resolve", {
                    "apt_id": apt_id,
                    "appointment_id": appointment['appointment_id'],
                    "issue_id": appointment['issue_id'],
                })
                if response.status_code == 200:
                    st.success("Appointment resolved successfully!")
                    st.rerun()
                else:
                    st.error("Failed to resolve appointment.")

def scheduled_repairmen_appointments():
    user:User = st.session_state['user']
    if user.get_user_type() != UserType.REPAIRMEN:
        return
    appointments = json.loads(sendGetReq("/repairmen/appointments", {"repairmen_id": user.user_id}).text)
    if len(appointments) == 0:
        st.text("No appointments scheduled yet")
    else:
        for appointment in appointments:
            display_appointment_for_repairmen(appointment)

def show_repairmen_details():
    st.header("My Appointments")
    scheduled_repairmen_appointments()
    st.header("Active Issues")
    active_issues()

def active_issues():
    user:User = st.session_state['user']
    if user.get_user_type() != UserType.REPAIRMEN:
        return
    issues: List = json.loads(sendGetReq("/repairmen/issues").text)
    if len(issues) == 0:
        st.text("No active issues")
    else:
        for issue in issues:
            display_issue_for_repairmen(issue)
            appointment_date = st.date_input("When can you work on this issue?", key=str(issue['issue_id'])+"date", min_value=datetime.date.today())
            duration = st.number_input("How long (in hours) will it take for you to fix it?", key=str(issue['issue_id'])+"duration", step = 0.5, min_value = float(0.5))
            charge = st.number_input("How much can you charge (in dollars) for it?", disabled=True, value=28*duration, key=str(issue['issue_id'])+"charge")
            if st.button(f"Commit", key = str(issue['issue_id'])+"commit"):
                response = sendPostReq("/repairmen/commit", {}, {
                    "apt_id": issue['apt_id'],
                    "issue_id": issue['issue_id'],
                    "appointment_date": appointment_date.isoformat(),
                    "duration": duration,
                    "charges": charge,
                    "repairmen_id": user.user_id,
                })
                if response.status_code == 200:
                    st.success("Appointment scheduled successfully!")
                    st.rerun()
                else:
                    st.error("Failed to schedule appointment.")
            st.text("")

def show_dashboard():
    user:User = st.session_state['user']
    user_type = user.get_user_type()
    st.title(f"{user_type} Dashboard")
    if ('just_logged_in' in st.session_state) and st.session_state['just_logged_in']:
        st.success("Login successful!")
        st.session_state['just_logged_in'] = False
    st.subheader("Welcome " + user.name + " !!!")
    st.write("")

    if user_type == UserType.TENANT:
        show_tenant_details()
    elif user_type == UserType.OWNER:
        create_apartment_owner()
        show_owner_details()
    elif user_type == UserType.BROKER:
        show_broker_details()
    elif user_type == UserType.REPAIRMEN:
        show_repairmen_details()
    