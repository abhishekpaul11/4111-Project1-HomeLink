import streamlit as st

from src.streamlit_app.formatting.marketplace import display_apt
from src.utils.reqs import sendPostReq


def show_offer_form():
    if 'selected_apt' in st.session_state:
        apt = st.session_state.selected_apt

        st.title("Apartment of Interest")
        display_apt(apt)

        st.title("Enter Offer Details")

        with st.form("offer_form"):
            offered_price = st.number_input("Offered Rent (in dollars)", min_value=1, value=apt['apt_rent'], step=100)
            duration = st.selectbox("Duration (in months)", range(1, 25))

            if st.form_submit_button('Submit Offer'):
                offer_data = {
                    "apt_id": apt['apt_id'],
                    "tenant_id": st.session_state.user.user_id,
                    "duration": duration,
                    "offered_price": offered_price,
                }
                response = sendPostReq("tenants/create_offer", offer_data)
                if response.status_code == 200:
                    st.success("Offer submitted successfully!")
                else:
                    st.error("Failed to submit offer. Duplicate offers not allowed.")

        if st.button("Go Back"):
            st.session_state['current_page'] = 'Dashboard'
            st.rerun()
    else:
        st.error("No apartment selected for creating an offer.")