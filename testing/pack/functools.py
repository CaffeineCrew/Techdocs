import json
import requests
BASE_URL = 'https://testing.api'

def get_access_token(data, return_refresh_token=False):
    """
def get_access_token(data, return_refresh_token=False):
    """
    try:
        url = BASE_URL + '/auth/login'
        headers = {'accept': 'application/json'}
        data = json.dumps(data)
        response = requests.post(url, data=data, headers=headers)
        access_token = response.json()['access_token']
        if return_refresh_token:
            refresh_token = response.json()['refresh_token']
            return (access_token, refresh_token)
        return access_token
    except Exception as e:
        print('Invlaid Credentials')
        return None

def request_inference(config, code_block, max_retries=1):
    """
    This function sends a POST request to the API server for code inference.

    Arguments:
    config (dict): A dictionary containing the necessary authentication details.
    code_block (str): The code block for which inference is requested.
    max_retries (int, optional): The maximum number of retries for the request. Defaults to 1.

    Returns:
    str: The docstring of the inferred code block returned from the API server. If the function doesn't receive a 200 status code
    after max_retries, it returns None.

    Raises:
    Exception: If the function encounters an error during the request and has no more retries left.
    """
    if max_retries == 0:
        return None
    url = BASE_URL + '/api/inference'
    headers = {'accept': 'application/json', 'Authorization': f"Bearer {config['access_token']}"}
    code_input = code_block
    response = requests.post(url=url, headers=headers, data=json.dumps({'code_block': code_input, 'api_key': config['api_key']}))
    if response.status_code == 200:
        return response.json()['docstr']
    else:
        data = {'username': config['username'], 'password': config['password']}
        print('Encountered error retrying...')
        config.update({'access_token': get_access_token(data)})
        return request_inference(config, code_block, max_retries=max_retries - 1)

def update_file(file_path, docstr_code):
    """
    Updates the docstring of a Python file.

    Arguments:
    file_path (str): The path of the Python file to be updated.
    docstr_code (str): The new docstring to replace the existing one.

    Returns:
    None

    Raises:
    FileNotFoundError: If the specified file does not exist.
    """
    with open(file_path, 'w', errors='ignore') as file:
        file.write(docstr_code)

def issue_api_key(config):
    """
    This function generates a new API key for the given user.

    Arguments:
    config: A dictionary containing the user's configuration.
        - access_token: str, The user's access token.
        - username: str, The user's username.

    Returns:
    None

    Raises:
    Exception, If the API key generation fails.
    """
    try:
        headers = {'accept': 'application/json', 'Authorization': f"Bearer {config['access_token']}"}
        response = requests.put(url=BASE_URL + '/auth/regenerate_api_key', headers=headers, data=json.dumps({'username': config['username']}))
        if response.status_code != 200:
            raise Exception('API Key Generation Failed')
        print(f"$ API_KEY:{response.json()['api_key']}")
    except Exception as e:
        print(f'$ {e}')

def signup(config):
    """
def signup(config: dict) -> None:
    """
    try:
        headers = {'accept': 'application/json'}
        response = requests.post(url=BASE_URL + '/auth/signup', headers=headers, data=json.dumps(config))
        if response.status_code == 226:
            raise Exception('username or email already exists')
        elif response.status_code != 200:
            raise Exception('Something went wrong, please try again later')
        print('Signed up successfully, please issue a new `API_KEY` to continue')
    except Exception as e:
        print(e)