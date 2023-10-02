import json
import streamlit as st

def authors():
    # {"Github → " "["username"]" "("url")" for username,url in author_details["socials"].items() }
    # with open("frontend/contend/authors.json","r") as f:
    #     author_details = json.load(f)
    st.sidebar.divider()
    st.sidebar.info(
    """
    Follow us on:
    
    Github → [@mayureshagashe2105](https://github.com/MayureshAgashe2105)\n
    Github → [@HemanthSai7](https://github.com/HemanthSai7)
    """
    )