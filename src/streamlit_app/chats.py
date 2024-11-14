import streamlit as st
from flask import json

from src.utils.reqs import sendGetReq

def get_chats():
    return json.loads(sendGetReq("tenant/get_chats", {"tenant_id": st.session_state.user.user_id}).text)

def show_chats():
    chats = get_chats()

    if not chats:
        st.write("No ongoing chats found. Go to the Marketplace to start negotiating on an Apartment. Happy Browsing !!!")
        return

    st.title('Chats')

    st.write("")
    st.write("")

    for chat in chats:
        button = st.button(f'Apartment {chat['apt_id']}', key=chat['apt_id'])
        st.write("")

        if button:
            st.session_state.current_page = 'Messages'
            st.session_state.current_chat = chat
            st.rerun()