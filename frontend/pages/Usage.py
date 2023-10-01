import streamlit as st
from Login import auth_page
from PIL import Image

st.set_page_config(
    page_title="Usage",
    layout="wide",
    page_icon="📝",
    initial_sidebar_state="expanded",
)

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

def usage():
    st.markdown("### :rainbow[How to use Techdocs?]")

    col1,col2 = st.columns(2,gap="small")

    with col1:

        img = Image.open("frontend/images/image.png")
        st.image(img)

        st.caption("Boat sailing in the sea")

    with col2:
        intro_text="""
        Now that you've arrived at this digital crossroads, you're most likely eager to dive into the world of Techdocs. Great choice! In today's fast-paced tech landscape, having well-structured and easily accessible documentation is like having a treasure map to navigate the vast ocean of code. You are probably wondering how to use Techdocs.  
        """

        text="""
        But you might be wondering: "How do I embark on this documentation journey with Techdocs?" Fear not, because we're about to chart a course through the fascinating world of Techdocs, where clarity, efficiency, and ease-of-use are the guiding stars.
        """
        st.write(f'<p style="font-size:22px; color:#9c9d9f ">{intro_text}</p>', unsafe_allow_html=True)
        st.write(f'<p style="color:#9c9d9f; font-size:22px">{text}</p>', unsafe_allow_html=True)

    st.markdown("### 📝 :rainbow[Using Techdocs via the CLI]")  
    st.info("Please use the CLI to generate the documentation for your project. The Streamlit app is just a preview to give the user an idea of the project.")  
    st.warning("To start using the CLI, please generate an API Key from the Streamlit app. You can also generate the API Key from the CLI.")

    with st.expander("⚙️ Installation and setup",expanded=True):
        st.write("1. Create a virtual environment. We recommend using conda but you can python's venv as well:"); st.code("conda create -n techdocs python=3.11","python")
        st.write("2. Install Techdocs via pip:"); st.code("pip install techdocs","python")
        st.write("3. CD into your project directory.")
        st.code("CD <YOUR-PROJECT-DIRECTORY>","bash")

    with st.expander("🚀 CLI and Working", expanded=True):
        st.write("1. Once the installation is complete, type **techdocs** in the terminal. You should be able to see info about our CLI.")
        st.write("2. You can login into our Techdocs app using the CLI or create an account if you don't have one. To signup, type the following command in the terminal:")
        st.code("techdocs signup -u <username> -p <password> -e <email>", "bash")
        st.write("3. Generate an API Key from the Code page and paste it in the command below.")
        st.code("techdocs generate -k <API_KEY> -u <USERNAME> -p <PASSWORD> -d <ROOT-DIRECTORY-OF-THE-PROJECT>","bash")
        st.write("4. Wait for the documentation to be generated. You can view the status of the documentation generation in the CLI.")   

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
    st.session_state.runpage = usage
st.session_state.runpage()                
