import streamlit as st
from flask import json

from src.streamlit_app.formatting.marketplace import display_apt
from src.utils.reqs import sendGetReq


def display_formatted_info(apartments):
    if apartments:
        st.title("Available Apartments")
        for apt in apartments:
            display_apt(apt)
            if st.button("Make an offer", key=apt['apt_id']):
                st.session_state['selected_apt'] = apt
                st.session_state['current_page'] = 'Offers'
                st.rerun()
    else:
        st.write("No Apartments Available")

def get_apartments():
    return json.loads(sendGetReq("tenants/available_apts", {"offset": st.session_state.offset}).text)

def get_apartment_count():
    return json.loads(sendGetReq("tenants/available_apts_count", {}).text)

def show_marketplace():

    if 'offset' not in st.session_state:
        st.session_state.offset = 0

    if 'total_apts' not in st.session_state:
        st.session_state.total_apts = 21

    display_formatted_info(get_apartments())

    col1, col2 = st.columns(2)

    with col2:
        if st.button('Next', disabled=(st.session_state.offset + 10 > st.session_state.total_apts)):
            if st.session_state.offset + 10 <= st.session_state.total_apts:
                st.session_state.offset += 10
                st.rerun()

    with col1:
        if st.button('Prev', disabled=(st.session_state.offset - 10 < 0)):
            if st.session_state.offset - 10 >= 0:
                st.session_state.offset -= 10
                st.rerun()