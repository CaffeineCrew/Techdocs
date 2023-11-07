import streamlit as st
from PIL import Image
from layouts.mainlayout import mainlayout

@mainlayout
def instructions():
    """
    This function displays instructions for installing and using Techdocs via the CLI.

    It reads the installation and working instructions from specified Markdown files and
    displays them using Streamlit's markdown and expander components.

    The function is designed to provide a user-friendly interface for demonstrating the
    usage of Techdocs via the CLI.

    No return value. This function only displays instructions and does not return any value.

    Raises:
    FileNotFoundError: If the specified Markdown files are not found.

    """
    with open('frontend/content/installation.md', 'r', encoding='utf-8') as f:
        instructions = f.read()
    with open('frontend/content/working.md', 'r', encoding='utf-8') as f:
        working = f.read()
    st.markdown('### 📝 :rainbow[Using Techdocs via the CLI]')
    st.info('Please use the CLI to generate the documentation for your project. The Streamlit app is just a demo to give the user an idea of the project.')
    with st.expander('⚙️ Installation and setup'):
        st.markdown(instructions)
    with st.expander('🚀 CLI and Working', expanded=True):
        st.markdown(working)