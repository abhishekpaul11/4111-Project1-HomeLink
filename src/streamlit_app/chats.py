import streamlit as st
from flask import json

from src.utils.reqs import sendGetReq

def get_chats():
    if st.session_state.user.is_tenant:
        return json.loads(sendGetReq("tenant/get_chats", {"tenant_id": st.session_state.user.user_id}).text)
    elif st.session_state.user.is_owner or st.session_state.user.is_broker:
        return json.loads(sendGetReq("manager/get_chats", {"manager_id": st.session_state.user.user_id}).text)

def show_chats():
    chats = get_chats()

    if not chats:
        if st.session_state.user.is_tenant:
            st.write("No ongoing chats found. Go to the Marketplace to start negotiating on an Apartment. Happy Browsing !!!")
        else:
            st.write("No ongoing chats found. Chats will show up here if any prospective tenant is interested in an"
                     " apartment directly managed by you.")
        return

    st.title('Chats')

    st.write("")
    st.write("")

    title = ''

    for chat in chats:

        if st.session_state.user.is_tenant:
            button_text = f'Apartment {chat['apt_id']} ({chat["apt_address"]})'
        else:
            if title != f'Apartment {chat["apt_id"]}':
                title = f'Apartment {chat["apt_id"]}'
                st.header(title)
                st.write(chat["apt_address"])
                st.write("")
                st.write("")

            button_text = f'Tenant {chat["tenant_id"]}'

        button = st.button(button_text, key=str(chat['apt_id']) + str(chat['tenant_id']))
        st.write("")

        if button:
            st.session_state.current_page = 'Messages'
            st.session_state.current_chat = chat
            st.rerun()