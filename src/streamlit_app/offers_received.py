from datetime import datetime

import streamlit as st
from flask import json

from src.streamlit_app.formatting.offers_received import display_offer
from src.utils.reqs import sendGetReq, sendDelReq, sendPostReq


def display_formatted_info(offers):
    if offers:
        st.title("Offer(s) Received")
        for offer in offers:
            display_offer(offer)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Accept Offer", key=str(offer['offer_id'])+'_accept'):
                    offer['rented_date'] = datetime.now().strftime("%B %d, %Y")

                    response = sendPostReq("owner/accept_offer", offer)
                    if response.status_code == 200:
                        st.success("Offer accepted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to accept offer.")
            with col2:
                if st.button("Reject Offer", key=str(offer['offer_id'])+'_reject'):
                    response = sendDelReq("owner/delete_offer", offer)
                    if response.status_code == 200:
                        st.success("Offer rejected successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to reject offer.")

    else:
        st.write("No offers available on the apartments directly managed by you.")

def get_offers():
    return json.loads(sendGetReq("owner/get_offers", {"owner_id": st.session_state.user.user_id}).text)

def show_offers():
    display_formatted_info(get_offers())