import json
import requests
from PIL import Image

import streamlit as st
from Login import auth_page

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Built by @HemanthSai7 and @MayureshAgashe2107 with Streamlit"},
)

st.markdown("## :rainbow[Welcome to Techdocs: Where Code Meets Clarity!] 🚀")



def logout():
    del st.session_state["access_token"]
    del st.session_state["refresh_token"]
    del st.session_state["username"]

def instructions():
    with st.expander("📝Instructions",expanded=True):
        st.markdown(
            """
            ##### 1. Generate an `API Key` from the sidebar to get started.

            ##### 2. Paste the  `API Key` in the field provided.

            ##### 3. Paste your code function in the input code box.

            ##### 4. Click on the `Generate Documentation` 🤖 button to generate the documentation.
            
            ##### 5. The generated documentation will be displayed in the section below.

            """
        ) 


with st.sidebar:
    if 'username' not in st.session_state:
        with st.expander("🧑Account Details",expanded=True):
            st.header("Please Login or Signup to continue")
    else:
        
        with st.expander("🔑 TECHDOCS-API-KEY",expanded=True):
            st.warning("Generating a new API Key will invalidate the previous one from all your projects. Do you wish to continue?")
            if st.button("Generate API KEY"):
                with st.spinner("Generating API Key..."):
                    try:
                        base_url = "http://localhost:8000"
                        headers={"accept":"application/json", "Authorization": f"Bearer {st.session_state.access_token}"}
                        response = requests.put(url=base_url + "/auth/regenerate_api_key", headers=headers, data=json.dumps({"username":st.session_state.username}))
                        if (response.status_code!=200):
                            raise Exception("API Key Generation Failed")
                        st.info("Please save the API KEY as it will be shown only once.")
                        st.code(response.json()["api_key"],"bash")
                        st.success("API Key Generated Successfully")
                    except Exception as e:
                        st.error(e)
        


        with st.expander("🧑Account Details",expanded=True):
            st.info(f"Welcome, {st.session_state.username}! 😄")
            if st.button("Logout 👋"):
                logout()
                st.rerun()


def code_page():
    base_url = 'http://localhost:8000'

    def query_post(url, headers, data=None, params=None):
        response = requests.post(url, data=data, headers=headers, params=params)
        return response
    
    headers={"accept":"application/json"}

    instructions()
    st.warning("Hi there! Paste your TECHDOCS-API-KEY in the field below to get started!\n\n", icon="🚨")
    API_KEY = st.text_input(label="Enter your API key", label_visibility="hidden",placeholder="Enter your API key", type="password")
  

    code_input = st.text_area("Code Input", height=300, help="Paste your code here")
    comment_placeholder = st.empty()

    if st.button("🤖 Generate Documentation"):
        if code_input:
            headers['Authorization'] = f"Bearer {st.session_state.access_token}"
            response = query_post(base_url + '/api/inference', headers=headers, params={'code_block':code_input, 'api_key':API_KEY})
            docstr = response.json()["docstr"]
            comment_placeholder.subheader("Generated Documentation:")
            comment_placeholder.markdown(f"<pre><code>{docstr}</code></pre>", unsafe_allow_html=True)
            # Scroll to the comment section
            comment_placeholder.empty()
            comment_placeholder.markdown(f"<pre><code>{docstr}</code></pre>", unsafe_allow_html=True)
        else:
            st.warning("Please enter some code.")


if 'access_token' not in st.session_state:
    st.session_state.runpage = auth_page  
else:
    st.session_state.runpage = code_page
st.session_state.runpage()