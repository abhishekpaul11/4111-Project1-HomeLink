import json

import streamlit as st
from src.utils.reqs import sendGetReq, sendPostReq


def add_tenant_message(message):
    with st.chat_message(avatar='🧑‍💻', name='human'):
        st.html(f"<span class='chat-human'></span>")
        st.write(message)

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
        st.write(message)

def fetch_messages():
    return json.loads(sendGetReq("tenant/get_messages",
                                 {"chat_id": st.session_state.current_chat['chat_id'], "apt_id": st.session_state.current_chat['apt_id']}).text)

def show_messages():

    if st.button("Home"):
        st.session_state['current_page'] = 'Dashboard'
        st.rerun()

    messages = fetch_messages()
    chat = st.session_state.current_chat

    st.title(f'Apartment {chat["apt_id"]}')

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
            "is_from_tenant": True,
        }

        response = sendPostReq("tenant/send_message", message_data)

        if response.status_code == 200:
            st.success("Message sent successfully!")
            st.rerun()
        else:
            st.error("Failed to send message. Please try again.")
            st.rerun()