import json

import streamlit as st
from src.utils.reqs import sendGetReq, sendPostReq
from streamlit_autorefresh import st_autorefresh


def add_tenant_message(message):
    with st.chat_message(avatar='🧑‍💻', name='human'):
        st.html(f"<span class='chat-human'></span>")
        st.write(message)

    if st.session_state.user.is_tenant:
        st.html(
            """
                <style>
                    .stChatMessage:has(.chat-human) {
                        flex-direction: row-reverse;
                        text-align: right;
                    }
                </style>
            """
        )

def add_apartment_message(message):
    with st.chat_message(avatar='🏠', name='user'):
        st.html(f"<span class='chat-user'></span>")
        st.write(message)

    if not st.session_state.user.is_tenant:
        st.html(
            """
                <style>
                    .stChatMessage:has(.chat-user) {
                        flex-direction: row-reverse;
                        text-align: right;
                    }
                </style>
            """
        )

def fetch_messages():
    return json.loads(sendGetReq("tenant/get_messages",
                                 {"chat_id": st.session_state.current_chat['chat_id'], "apt_id": st.session_state.current_chat['apt_id']}).text)

def show_messages():

    st_autorefresh(interval=2000, key="auto_refresh")

    if st.button("Home"):
        st.session_state['current_page'] = 'Dashboard'
        st.rerun()

    messages = fetch_messages()
    chat = st.session_state.current_chat

    st.title(f'Apartment {chat["apt_id"]}')
    st.write(chat['apt_address'])
    if not st.session_state.user.is_tenant: st.header(f'Tenant {chat["tenant_id"]}')

    if messages:
        for message in messages:
            if message['is_from_tenant']:
                add_tenant_message(message['content'])
            else:
                add_apartment_message(message['content'])
    else:
        st.write("Send a message to start the conversation.")

    if prompt := st.chat_input('Ask something...'):
        message_data = {
            "apt_id": chat['apt_id'],
            "chat_id": chat['chat_id'],
            "content": prompt,
            "is_from_tenant": st.session_state.user.is_tenant
        }

        response = sendPostReq("tenant/send_message", message_data)

        if response.status_code == 200:
            st.success("Message sent successfully!")
            st.rerun()
        else:
            st.error("Failed to send message. Please try again.")
            st.rerun()