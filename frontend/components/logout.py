import streamlit as st

def logout():
    """
    This function logs out the current user by deleting their access token, refresh token, and username from the session.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    del st.session_state['access_token']
    del st.session_state['refresh_token']
    del st.session_state['username']