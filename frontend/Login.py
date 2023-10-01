import json
import requests

import streamlit as st
        

def auth_page():

    base_url = 'https://caffeinecrew-techdocs.hf.space'


    headers={"accept":"application/json"}

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        with st.form(key="myform2"):
            username = st.text_input(label="Username", label_visibility="collapsed", placeholder="Username")
            password = st.text_input(label="Password", label_visibility="collapsed", placeholder="Password", type="password")
            login_button = st.form_submit_button(label="Login")

        with st.spinner("Logging in..."):
            if login_button:
                try:
                    credentials = {"username":username, "password":password}
                    response = requests.post(base_url + "/auth/login", headers=headers, data=json.dumps(credentials)) 
                    if (response.status_code!=200):
                        raise Exception("Login Failed")
                    # res_dict.update(response.json())
                    st.session_state["username"] = username
                    st.session_state["access_token"] = response.json()['access_token']
                    st.session_state["refresh_token"] = response.json()['refresh_token']
                    st.success("Logged in successfully")
                    st.rerun()

                except Exception as e:
                    st.error(e)

    with tab2:
        with st.form(key="myform1"):
            username = st.text_input(label="Username", label_visibility="collapsed", placeholder="Username")
            password = st.text_input(label="Password", label_visibility="collapsed", placeholder="Password", type="password")
            email = st.text_input(label="Email", label_visibility="collapsed", placeholder="Email")
            signup_button = st.form_submit_button(label="Signup")

        with st.spinner("Signing up..."):
            if signup_button:
                try:
                    credentials = {"username":username, "password":password, "email":email}
                    response = requests.post(url=base_url + "/auth/signup", headers=headers, data=json.dumps(credentials))
                    if (response.status_code!=200):
                        raise Exception("Signup Failed")
                
                    st.success("Signed up successfully")
                except:
                    st.error("Signup Failed")   


st.sidebar.divider()
st.sidebar.info(
    """
    Follow us on:

    Github → [@mayureshagashe2105](https://github.com/MayureshAgashe2105)\n
    Github → [@HemanthSai7](https://github.com/HemanthSai7)
    """
)
            



