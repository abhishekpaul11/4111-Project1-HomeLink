# streamlit_app/login.py
import streamlit as st
from login import show_login
from dashboard import show_dashboard

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Login"

def sidebar():
    if st.session_state['authenticated']:
        st.sidebar.title("Navigation")
        choice = st.sidebar.radio("Go to", ["Dashboard", "Logout"])
        
        if choice == "Dashboard":
            st.session_state['current_page'] = "Dashboard"
        elif choice == "Logout":
            st.session_state['authenticated'] = False
            st.session_state['current_page'] = "Login"
            st.session_state['username'] = None
            st.rerun(scope="app")

# Display the correct page
def main():
    sidebar()
    
    if st.session_state['current_page'] == "Login":
        show_login()
    elif st.session_state['current_page'] == "Dashboard":
        show_dashboard()

# Run the main function
if __name__ == "__main__":
    main()