import streamlit as st
from PIL import Image

from layouts.mainlayout import mainlayout

@mainlayout
def instructions():
    with open("content/installation.md", "r",encoding='utf-8') as f:
        instructions = f.read()

    with open("content/working.md", "r",encoding='utf-8') as f:
        working = f.read()
    

    st.markdown("### 📝 :rainbow[Using Techdocs via the CLI]")  
    st.info("Please use the CLI to generate the documentation for your project. The Streamlit app is just a demo to give the user an idea of the project.")  
    st.warning("To start using the CLI, please generate an API Key from the Streamlit app. You can also generate the API Key from the CLI.")

    with st.expander("⚙️ Installation and setup"):
        st.markdown(instructions)

    with st.expander("🚀 CLI and Working", expanded=True):
        st.markdown(working)              
