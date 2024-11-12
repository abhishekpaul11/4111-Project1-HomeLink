# streamlit_app/login.py
import time
from flask import json
import streamlit as st
from login import show_login
from dashboard import show_dashboard
from src.popo.User import User
from src.streamlit_app.marketplace import show_marketplace
from src.streamlit_app.offers import show_offer_form
from src.streamlit_app.offers_received import show_offers
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
        user = User(**user_data)
        st.session_state['user'] =user 
        st.session_state['current_page'] = "Dashboard"
        st.session_state['authenticated'] = True

def sidebar():
    if st.session_state['authenticated']:
        st.sidebar.title("Navigation")

        if st.session_state['user'].is_tenant:
            option = ["Dashboard", "Marketplace", "Logout"]
        else:
            option = ["Dashboard", "Offers", "Logout"]
        choice = st.sidebar.radio("Go to", option)

        if choice == "Dashboard":
            st.session_state['current_page'] = "Dashboard"
        elif choice == "Logout":
            st.session_state['authenticated'] = False
            st.session_state['current_page'] = "Login"
            st.session_state['username'] = None

            localS.deleteItem("user")
            time.sleep(0.5)
            st.rerun(scope="app")
        elif choice == "Marketplace":
            st.session_state['current_page'] = "Marketplace"
        elif choice == "Offers":
            st.session_state['current_page'] = "Offers Received"


# Display the correct page
def main():

    # Hack to implement routing from marketplace to offers
    if st.session_state.current_page == "Offers":
        show_offer_form()
        return

    sidebar()
    
    if st.session_state['current_page'] == "Login":
        show_login()
    elif st.session_state['current_page'] == "Dashboard":
        show_dashboard()
    elif st.session_state['current_page'] == "Marketplace":
        show_marketplace()
    elif st.session_state['current_page'] == "Offers Received":
        show_offers()


# Run the main function
if __name__ == "__main__":
    main()