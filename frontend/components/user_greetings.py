import streamlit as st
from .logout import logout

def user_greetings():
    """
    Displays a welcome message for the logged-in user or prompts them to login/signup.

    This function displays a sidebar expander with the user's welcome message if they are logged in.
    If the user is not logged in, it warns them to login/signup to continue.

    The function also includes a logout button for the logged-in user, which will log them out and rerun the current page.

    Arguments:
    - None

    Returns:
    - None

    Raises:
    - None
    """
    with st.sidebar.expander('🧑Account Details', expanded=True):
        if 'username' not in st.session_state:
            st.warning('Please Login or Signup to continue')
        else:
            st.info(f'Welcome, {st.session_state.username}! 😄')
            if st.button('Logout 👋'):
                logout()
                st.rerun()