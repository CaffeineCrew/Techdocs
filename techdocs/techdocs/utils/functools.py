import json
import requests
BASE_URL = 'https://caffeinecrew-techdocs.hf.space'

def get_access_token(data, return_refresh_token=False):
    """
    This function is used to get an access token and refresh token for the given data.

    Args:
        data: A dictionary containing the credentials required for authentication.
        return_refresh_token: A boolean flag indicating whether to return the refresh token along with the access token. Defaults to False.

    Returns:
        If return_refresh_token is False, it returns the access token (str). If return_refresh_token is True, it returns a tuple containing the access token and the refresh token (Tuple[str, str]).

    Raises:
        None
    """

def get_access_token(data, return_refresh_token=False):
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

        if response.json() == "exception.InvalidCredentialsException()":  
            print("Please check your credentials")
        else:
            print('Please verify your email before logging in')
        return None


def request_inference(config, code_block, max_retries=1):
    """
Request Inference
==================

This function sends a POST request to the API server to request the inference of a given code block.

### Parameters

* **config** (dict): A dictionary containing the necessary configuration details such as access_token, api_key, and username.
* **code_block** (str): The code block for which inference is requested.
* **max_retries** (int, optional): The maximum number of times the function should retry in case of an error. Defaults to 1.

### Returns

* **str**: Returns the docstring of the inference result in the form of a string. If the function fails after all retries, it returns None.

### Raises

* **requests.exceptions.HTTPError**: If the server returns a status code other than 200.
* **requests.exceptions.RequestException**: If there is an error during the request.
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
    Updates the documentation string in the specified file.

    Arguments:
    file_path (str): The path to the file where the documentation string will be written.
    docstr_code (str): The documentation string to be written to the file.

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
    config (dict): A dictionary containing the user's configuration.
        - access_token (str): The user's access token.
        - username (str): The user's username.

    Returns:
    None: This function doesn't return anything, it prints the new API key.

    Raises:
    Exception: If the API key generation fails, an exception with the message 'API Key Generation Failed' is raised.
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

        print(response.json()["message"][0].replace('\\n','\n'), "Then issue a new `API_KEY` to continue")

    except Exception as e:
        print(e)