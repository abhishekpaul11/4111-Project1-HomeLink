import streamlit as st
from flask import json

from src.streamlit_app.formatting.marketplace import display_apt
from src.utils.reqs import sendGetReq, sendPostReq


def display_formatted_info(apartments):
    if apartments:
        st.title("Available Apartments")
        for apt in apartments:
            st.header(f'Apartment {apt['apt_id']}')
            display_apt(apt)

            col1, col2 = st.columns(2)

            with col1:
                if not st.session_state['is_lease_on'] and st.button("Make an offer", key=str(apt['apt_id'])+'_offer'):
                    st.session_state['selected_apt'] = apt
                    st.session_state['current_page'] = 'Offers'
                    st.rerun()

            with col2:
                if st.button("Contact", key=str(apt['apt_id'])+'_chat'):
                    create_or_open_chat(apt['apt_id'])

    else:
        st.write("No Apartments Available")

def create_or_open_chat(apt_id):

    chat = get_chat(apt_id)
    if chat and len(chat) > 0:
        navigate_to_chat(chat[0])

    else:
        chat_data = {
            "apt_id": apt_id,
            "tenant_id": st.session_state['user'].user_id,
        }

        sendPostReq("tenant/create_chat", chat_data)

        chat = get_chat(apt_id)
        if chat and len(chat) > 0:
            navigate_to_chat(chat[0])
        else:
            st.error("Some issue encountered. Try again")

def navigate_to_chat(chat):
    st.session_state.current_page = 'Messages'
    st.session_state.current_chat = chat
    st.rerun()

def get_chat(apt_id):
    return json.loads(sendGetReq("tenant/get_chat_by_apt", {"tenant_id": st.session_state.user.user_id, 'apt_id': apt_id}).text)

def get_apartments():
    return json.loads(sendGetReq("tenants/available_apts", {"offset": st.session_state.offset}).text)

def get_apartment_count():
    return json.loads(sendGetReq("tenants/available_apts_count", {}).text)

def show_marketplace():

    if 'offset' not in st.session_state:
        st.session_state.offset = 0

    if 'total_apts' not in st.session_state:
        st.session_state.total_apts = get_apartment_count()['count']

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