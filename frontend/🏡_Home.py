import streamlit as st
from layouts.mainlayout import mainlayout

@mainlayout
def home():
    st.subheader("Code documentation tool that works in your IDE like magic!")

    def changestate(*args):
        st.session_state[args[0]]=True

    tab1, tab2, tab3 = st.tabs(["About our CLI 🪄", "Mechanics 🛠️", "LLMs toolkit 🗃️"])
    with tab1:
        st.markdown('### <div align="center">:green[Our CLI Tool 🧑‍💻]</div>',unsafe_allow_html=True)
        st.markdown('##### <div align="center">:blue[Techdocs CLI] provides a simple and easy to use interface to generate documentation for your :blue[code].</div>',unsafe_allow_html=True)
        col1, col3, col2 = st.columns([4,0.1,2])
        with col1:
            st.image("frontend/images/techdocs.png")
        with col2:
            st.checkbox("##### User friendly commands\n ✅ Easy to follow commands to generate documentation for your code.",value=True,key="feature1_a",on_change=changestate,args=("feature1_a",))
            st.checkbox("##### Your workbench at one place\n ✅ Access all commands within our CLI. No need to search the app.",value=True,key="feature1_b",on_change=changestate,args=("feature1_b",))
            st.checkbox("##### Generated documentation will be directly embedded into your functions\n ✅ No need to manually copy paste the documentation.",value=True,key="feature1_c",on_change=changestate,args=("feature1_c",))

    with tab2:
        st.markdown('### <div align="center">:green[API behind the Scenes ⚙️]</div>',unsafe_allow_html=True)
        st.markdown('#### <div align="center">:blue[CLI] uses the power of our API allowing you to access sophisticated :blue[LLM] tools effortlessly. This :blue[microservice] is deployed separately abstracting undelying complexities and providing lightweight web app and CLI </div>',unsafe_allow_html=True)
        col1, col3, col2 = st.columns([4,0.1,2])
        with col1:
            st.image("frontend/images/backendss.png")
        with col2:
            st.checkbox("##### API uses the magic of FastAPI⚡\n✅ FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.",value=True,key="backend_a",on_change=changestate,args=("backend_a",))
            st.checkbox("##### Deployed on Huggingface Spaces 🤗\n✅ Minimal user-percieved latency.",value=True,key="backend_b",on_change=changestate,args=("backend_b",))
            st.checkbox("##### Cloud Databases ☁️\n ✅ Powered by Microsoft Azure SQL",value=True,key="backend_c",on_change=changestate,args=("backend_c",))

    with tab3:
        st.markdown('### <div align="center">:green[Large Language Models 🦙]</div>',unsafe_allow_html=True)
        st.markdown('#### <div align="center">Combines the power of Langchain and Clarifai</div>',unsafe_allow_html=True)
        col1, col3, col2 = st.columns([4,0.1,2])
        with col1:
            st.image("frontend/images/llms.png")

        with col2:
            st.checkbox('##### WizardLM-70B at its core 🧙‍♂️.\n✅ Uses WizardLM-70B LLM as an endpoint provided by Clarifiai.',value=True,key="llm_a",on_change=changestate,args=("llm_a",))    
            st.checkbox("##### Application developed using Langchain 🦜.\n✅ LangChain is a framework for developing applications powered by language models.", value=True,key="llm_b",on_change=changestate,args=("llm_b",))


    st.markdown("## <div align='center'>Techdocs Architecture</div>",unsafe_allow_html=True)
    st.image("frontend/images/architecture.png")       
