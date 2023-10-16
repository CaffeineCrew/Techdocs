import json
import streamlit as st

from typing import Callable

from components import authors, user_greetings, login

def mainlayout(func: Callable):
    with open("frontend/layouts/st_page_layouts.json", "r",encoding='utf-8') as f:
        st_page_layouts = json.load(f)
    st.set_page_config(**st_page_layouts[f"{func.__name__}" if func.__name__ in st_page_layouts.keys() else "home"])
    add_logo("frontend/images/techdocslogo.svg",svg=True)
    st.markdown("## :rainbow[Welcome to Techdocs: Where Code Meets Clarity!]🚀")

    user_greetings()

    if 'access_token' not in st.session_state:
        st.session_state.runpage = login
    else:
        st.session_state.runpage = func
    
    def load_page():
        return st.session_state.runpage()
    load_page()
    authors()

      

