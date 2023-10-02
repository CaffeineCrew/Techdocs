import streamlit as st
from layouts.mainlayout import mainlayout

@mainlayout
def home_page():

    st.markdown(
    """
    ##### Unleash the documentation dynamo that is **Techdocs**! Say goodbye to the documentation drudgery that haunts coders' dreams and embrace the effortless power of AI-driven documentation. With **Techdocs**, harness the genius of LLama2 🦙, the magic of WizardCoderLM 🧙‍♂️, the versatility of Huggingface Transformers 🤗, and the precision of Langchain 🦜 and Clarifai 🤖.

    """
    )

    with st.expander("What Can Techdocs Do for You? 🌟",expanded=True):
        st.markdown(
        """
        - Boost your code quality effortlessly 🚀.
        - Effortlessly generate documentation for your code 🤖.
        - Include comments, descriptions, parameters, return values, and real-life examples 📃.
        - Elevate your code's readability, maintainability, and quality 📃.
        #
        """
        )
        