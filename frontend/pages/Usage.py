import streamlit as st
from Login import auth_page

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

        st.image("../assets/image.png",width=300,use_column_width=True)

        st.caption("Boat sailing in the sea")

    with col2:
        intro_text="""
        Now that you've arrived at this digital crossroads, you're most likely eager to dive into the world of Techdocs. Great choice! In today's fast-paced tech landscape, having well-structured and easily accessible documentation is like having a treasure map to navigate the vast ocean of code. You are probably wondering how to use Techdocs.  
        """

        text="""
        But you might be wondering: "How do I embark on this documentation journey with Techdocs?" Fear not, because we're about to chart a course through the fascinating world of Techdocs, where clarity, efficiency, and ease-of-use are the guiding stars.
        """
        st.write(f'<p style="font-size:20px; color:#9c9d9f ">{intro_text}</p>', unsafe_allow_html=True)
        st.write(f'<p style="color:#9c9d9f; font-size:20px">{text}</p>', unsafe_allow_html=True)

    st.markdown("### 📝 Using Techdocs via the CLI")    

    with st.expander("⚙️ Installation and setup",expanded=True):
        st.text("1. Create a virtual environment. We recommend using conda but you can python's venv as well:"); st.code("conda create -n techdocs python=3.11","python")
        st.text("2. Install Techdocs via pip:"); st.code("pip install techdocs","python")
        st.text("3. CD into your project directory.")
        st.code("CD <YOUR-PROJECT-DIRECTORY>","bash")
        st.text("""
                4. Login into our Techdocs Streamlit app or signup if you don't have an account.

                5. Generate an API Key from the Techdocs Streamlit app and paste it in the command below.
                """)
        st.code("techdocs -k <API_KEY> -u <USERNAME> -p <PASSWORD> -d <ROOT-DIRECTORY-OF-THE -PROJECT","bash")
        st.text("6. Wait for the documentation to be generated. You can view the status of the documentation generation in the CLI.")

    st.divider()
    st.markdown("### 📝 Using Techdocs via the Streamlit")

    with st.expander("📝Instructions",expanded=True):
        st.markdown(
            """
            ##### 1. Head over to the Code Page.

            ##### 2. Generate an `API Key` from the sidebar to get started.

            ##### 3. Paste the `API Key` in the field provided.

            ##### 4. Paste your code function in the input code box.

            ##### 5. Click on the `Generate Documentation`🤖 button to generate the documentation.
            
            ##### 6. The generated documentation will be displayed in the section below.

            """
        )      



if 'access_token' not in st.session_state:
    st.session_state.runpage = auth_page
else:
    st.session_state.runpage = usage
st.session_state.runpage()                