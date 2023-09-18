import streamlit as st
from Login import auth_page
from PIL import Image 

import base64

# image2=Image.open('assets/logo2.png')
st.set_page_config(
    page_title="DocGup-tea",
    layout="wide",
    page_icon="🏡",
    initial_sidebar_state="expanded",
)

@st.cache_data
def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# image = Image.open('assets/poster.jpg')
# st.image(image, caption='ELIGILOAN')

st.markdown("# :DocGup-tea: AI based Documentation Generator 📃")

def logout():
    del st.session_state["access_token"]
    del st.session_state["refresh_token"]
    del st.session_state["username"]

with st.sidebar:
    if 'username' not in st.session_state:
        st.header("Login/Signup")
    else:
        st.header(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            logout()
            st.experimental_rerun()


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

    set_page_background("../assets/bg.jpg") 

    st.markdown(
        """

        ## A step-by-step guide 

        The process is quite straightforward. BOB offers loans to eligible applicants with strong financial profiles. 
        Individuals need to provide their basic personal, employment, income and property details to know if you are fit to apply for a loan.

        ### 1 . Login 

        Step one is the login part, you just have to work your way through the following simple steps.
        - Enter your mobile number
        - Enter the OTP recieved 
        - accept consent in the Safe portal

        ### 2. Loan page

        Once you login, you will be redirected to the loan page.
        - Offer all relevant details such as loan amount, loan history, income, etc.
        - Click on the submit option once you have filled in all the details.
        - Our algorithm will assess your eligibility based on the details provided by you and you will be awarded with a `yes` or a `no`.
    """
    )

if 'access_token' not in st.session_state:
    st.session_state.runpage = auth_page
else:
    st.session_state.runpage = home_page
st.session_state.runpage()

