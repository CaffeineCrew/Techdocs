import streamlit as st
from .logout import logout

def user_greetings():
    with st.sidebar.expander("🧑Account Details",expanded=True):
        if 'username' not in st.session_state:
            st.warning("Please Login or Signup to continue")
        else:
            st.info(f"Welcome, {st.session_state.username}! 😄")
            if st.button("Logout 👋"):
                logout()
                st.rerun()