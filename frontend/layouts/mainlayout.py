import json
import streamlit as st
from typing import Callable
from components import authors, user_greetings, login, add_logo

def mainlayout(func: Callable):
    """
    This function sets the page configuration based on the function name passed as an argument.
    
    If the function name is not found in the 'st_page_layouts' dictionary, it defaults to the 'home' layout.
    
    The function also adds a logo to the page and displays a welcome message.
    
    If the user is not logged in, it redirects them to the login page. If the user is logged in, it executes the passed function.
    
    Arguments:
        func: A callable object. This argument is mandatory.
    
    Returns:
        None
    
    Raises:
        None
    """
    with open('frontend/layouts/st_page_layouts.json', 'r', encoding='utf-8') as f:
        st_page_layouts = json.load(f)
    st.set_page_config(**st_page_layouts[f'{func.__name__}' if func.__name__ in st_page_layouts.keys() else 'home'])
    add_logo('frontend/images/techdocslogo.svg', svg=True)
    st.markdown('## :rainbow[Welcome to Techdocs: Where Code Meets Clarity!]🚀')
    user_greetings()
    if 'access_token' not in st.session_state:
        st.session_state.runpage = login
    else:
        st.session_state.runpage = func

    def load_page():
        """
    This function loads a new page.

    Returns:
    None: This function does not return anything.
    """
        return st.session_state.runpage()
    load_page()
    authors()