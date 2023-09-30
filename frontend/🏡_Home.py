import streamlit as st
from Login import auth_page
from PIL import Image 
import textwrap

import base64

# image2=Image.open('assets/logo2.png')
st.set_page_config(
    page_title="Techdocs",
    layout="wide",
    page_icon="🏡",
    initial_sidebar_state="expanded",
)

@st.cache_data
def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.markdown("## :rainbow[Welcome to Techdocs: Where Code Meets Clarity!]🚀")

def logout():
    del st.session_state["access_token"]
    del st.session_state["refresh_token"]
    del st.session_state["username"]

with st.sidebar.expander("🧑Account Details",expanded=True):
    if 'username' not in st.session_state:
        st.warning("Please Login or Signup to continue")
    else:
        st.info(f"Welcome, {st.session_state.username}! 😄")
        if st.button("Logout 👋"):
            logout()
            st.rerun()


def home_page():


    def set_page_background(png_file):
        bin_str = get_base64_bin_file(png_file)
        page_bg_img = f'''
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{bin_str}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: scroll;
            }}
            </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

    # set_page_background("../assets/bg.jpg") 

    st.markdown(
        """

    ##### Unleash the documentation dynamo that is **Techdocs**! Say goodbye to the documentation drudgery that haunts coders' dreams and embrace the effortless power of AI-driven documentation. With **Techdocs**, harness the genius of LLama2, the magic of WizardCoderLM, the versatility of Huggingface Transformers, and the precision of Langchain and Clarifai.

    ## :rainbow[How Does Techdocs Work Its Magic?] 🔮

    ##### Just feed your code into **Techdocs**, and like a seasoned wizard, it'll conjure up beautifully detailed documentation in an instant. Your code will transform into a masterpiece of clarity, complete with insightful comments, vivid descriptions, crystal-clear parameters, return values, and real-world examples.

    """
    )

    with st.expander("What Can Techdocs Do for You? 🌟",expanded=True):
        st.markdown(
            """
        - ##### Boost your code quality effortlessly 🚀.
        - ##### Share your brilliance with the world in a snap 🌏.
        - ##### Effortlessly generate documentation for your code 🤖.
        - ##### Include comments, descriptions, parameters, return values, and real-life examples 📃.
        - ##### Elevate your code's readability, maintainability, and quality 📃.
        """
        )

    st.markdown(
        """
        ##### **Techdocs** is your code's trusty companion, helping you document with ease so you can focus on what you do best: coding!. **Techdocs** is your secret weapon for leveling up your code game. Whether you're a seasoned developer or just starting your coding journey, Techdocs has got your back. Get ready to unlock the future of code documentation today! 🌟
        """
    )

    st.markdown("""
                ## :rainbow[Ready to use Techdocs?]
                ##### Head over to the `Usage page` to get started!😄
                """)

    st.sidebar.divider()
    st.sidebar.info(
        """
        Follow us on:

        Github → [@mayureshagashe2105](https://github.com/MayureshAgashe2105)\n
        Github → [@HemanthSai7](https://github.com/HemanthSai7)
        """
    )


if 'access_token' not in st.session_state:
    st.session_state.runpage = auth_page
else:
    st.session_state.runpage = home_page
st.session_state.runpage()

