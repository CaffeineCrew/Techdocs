import json
import requests
import streamlit as st
from layouts.mainlayout import mainlayout

@mainlayout
def demo():

    def instructions():
        """
def instructions():
    """
        with st.expander('📝 Instructions', expanded=True):
            st.info('Please note that the Streamlit app is just a demo to give the user an idea of the project. To witness the full power of Techdocs, please use the CLI. The instructions to use the CLI are listed in Instructions page')
            st.markdown(
                """
                ##### 1. Generate an `API Key` from the sidebar to get started.

                ##### 2. Paste the  `API Key` in the field provided.

                ##### 3. Paste your `code function` in the input code box.

                ##### 4. Click on the `Generate Documentation` 🤖 button to generate the documentation.
                
                ##### 5. The `generated documentation` will be displayed in the section below.

                """
            )
    base_url = 'https://caffeinecrew-techdocs.hf.space'
    with st.sidebar:
        with st.expander('🔑 TECHDOCS-API-KEY', expanded=True):
            st.warning('Generating a new API Key will invalidate the previous one from all your projects. Do you wish to continue?')
            if st.button('Generate API KEY'):
                with st.spinner('Generating API Key...'):
                    try:
                        headers = {'accept': 'application/json', 'Authorization': f'Bearer {st.session_state.access_token}'}
                        response = requests.put(url=base_url + '/auth/regenerate_api_key', headers=headers, data=json.dumps({'username': st.session_state.username}))
                        if response.status_code != 200:
                            raise Exception('API Key Generation Failed')
                        st.info('Please save the API KEY as it will be shown only once.')
                        st.code(response.json()['api_key'], 'bash')
                        st.success('API Key Generated Successfully')
                    except Exception as e:
                        st.error(e)

    def query_post(url, headers, data=None, params=None):
        """
    Sends a POST request to the specified URL.

    Args:
        url (str): The URL to which the request is sent.
        headers (dict): A dictionary of HTTP headers to send with the request.
        data (dict, optional): Data to send in the request body. Defaults to None.
        params (dict, optional): Query parameters to append to the URL. Defaults to None.

    Returns:
        requests.Response: The response from the server.

    Raises:
        requests.exceptions.RequestException: If an error occurs while sending the request.

    """
        response = requests.post(url, data=data, headers=headers, params=params)
        return response
    headers = {'accept': 'application/json'}
    instructions()
    st.warning('Hi there! Paste your TECHDOCS-API-KEY in the field below to get started!\n\n', icon='🚨')
    API_KEY = st.text_input(label='Enter your API key', label_visibility='hidden', placeholder='Enter your API key', type='password')
    code_input = st.text_area('Code Input', height=300, help='Paste your code here')
    comment_placeholder = st.empty()
    if st.button('🤖 Generate Documentation'):
        with st.spinner('Generating Documentation...'):
            if code_input:
                headers['Authorization'] = f'Bearer {st.session_state.access_token}'
                response = query_post(base_url + '/api/inference', headers=headers, data=json.dumps({'code_block': code_input, 'api_key': API_KEY}))
                docstr = response.json()['docstr']
                comment_placeholder.subheader('Generated Documentation:')
                comment_placeholder.markdown(f'<pre><code>{docstr}</code></pre>', unsafe_allow_html=True)
                comment_placeholder.empty()
                comment_placeholder.markdown(f'<pre><code>{docstr}</code></pre>', unsafe_allow_html=True)
            else:
                st.warning('Please enter some code.')