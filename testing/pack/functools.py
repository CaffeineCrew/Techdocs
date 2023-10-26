import json
import requests
BASE_URL = 'https://caffeinecrew-techdocs.hf.space'

def get_access_token(data, return_refresh_token=False):
    """
    This function sends a POST request to the specified URL to get an access token.
    
    Arguments:
    data (dict): A dictionary containing the credentials required for authentication.
    return_refresh_token (bool, optional): A flag to indicate if the refresh token should be returned. Defaults to False.
    
    Returns:
    str or tuple: If return_refresh_token is False, the function returns the access token as a string. If return_refresh_token is True, the function returns a tuple containing the access token and the refresh token.
    
    Raises:
    Exception: If an error occurs during the execution of the function, an Exception is raised.
    """
    '\n    This function sends a POST request to the specified URL to get an access token.\n    \n    Arguments:\n    data (dict): A dictionary containing the credentials required for authentication.\n    return_refresh_token (bool, optional): A flag to indicate if the refresh token should be returned. Defaults to False.\n    \n    Returns:\n    str or tuple: If return_refresh_token is False, the function returns the access token as a string. If return_refresh_token is True, the function returns a tuple containing the access token and the refresh token.\n    \n    Raises:\n    Exception: If an error occurs during the execution of the function, an Exception is raised.\n    '
    '\n    This function sends a POST request to the specified URL to get an access token.\n    \n    Arguments:\n    data (dict): A dictionary containing the credentials required for authentication.\n    return_refresh_token (bool, optional): A flag to indicate if the refresh token should be returned. Defaults to False.\n    \n    Returns:\n    str or tuple: If return_refresh_token is False, the function returns the access token as a string. If return_refresh_token is True, the function returns a tuple containing the access token and the refresh token.\n    \n    Raises:\n    Exception: If an error occurs during the execution of the function, an Exception is raised.\n    '
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
Usage: request_inference(config, code_block, max_retries=1)

Purpose:
This function sends a POST request to the API server to perform code inference.

Arguments:
- config (dict): A dictionary containing the necessary authentication details like 'access_token', 'api_key' and 'username'.
- code_block (str): The code block that needs to be inferenced.
- max_retries (int, optional): The maximum number of times the function should retry in case of an error. Defaults to 1.

Returns:
- str: The docstring of the inferenced code block.

Raises:
- Exception: If the maximum number of retries (specified by max_retries) is reached and the API server still returns an error.
"""
    "\nUsage: request_inference(config, code_block, max_retries=1)\n\nPurpose:\nThis function sends a POST request to the API server to perform code inference.\n\nArguments:\n- config (dict): A dictionary containing the necessary authentication details like 'access_token', 'api_key' and 'username'.\n- code_block (str): The code block that needs to be inferenced.\n- max_retries (int, optional): The maximum number of times the function should retry in case of an error. Defaults to 1.\n\nReturns:\n- str: The docstring of the inferenced code block.\n\nRaises:\n- Exception: If the maximum number of retries (specified by max_retries) is reached and the API server still returns an error.\n"
    "\nUsage: request_inference(config, code_block, max_retries=1)\n\nPurpose:\nThis function sends a POST request to the API server to perform code inference.\n\nArguments:\n- config (dict): A dictionary containing the necessary authentication details like 'access_token', 'api_key' and 'username'.\n- code_block (str): The code block that needs to be inferenced.\n- max_retries (int, optional): The maximum number of times the function should retry in case of an error. Defaults to 1.\n\nReturns:\n- str: The docstring of the inferenced code block.\n\nRaises:\n- Exception: If the maximum number of retries (specified by max_retries) is reached and the API server still returns an error.\n"
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
    This function updates the docstring of a Python file.

    Arguments:
    file_path (str): The path of the Python file to be updated.
    docstr_code (str): The new docstring to be written to the file.

    Returns:
    None

    Raises:
    FileNotFoundError: If the specified file does not exist.
    IOError: If there is an error while writing to the file.
    """
    '\n    This function performs some operation on the given arguments.\n\n    Arguments:\n    arg1 (int): The first argument. A positive integer.\n    arg2 (float): The second argument. A positive floating point number.\n    arg3 (str): The third argument. A string containing only alphabets.\n    arg4 (bool): The fourth argument. A boolean value.\n\n    Returns:\n    None\n\n    Raises:\n    TypeError: If any argument is not of the expected type.\n    ValueError: If arg1 is less than or equal to zero, or if arg2 is not a positive number, or if arg3 contains any non-alphabetic character, or if arg4 is not a boolean value.\n    '
    '\n    This function updates the docstring of a Python file.\n\n    Arguments:\n    file_path (str): The path of the Python file to be updated.\n    docstr_code (str): The new docstring to be written to the file.\n\n    Returns:\n    None\n\n    Raises:\n    FileNotFoundError: If the specified file does not exist.\n    IOError: If there is an error while writing to the file.\n    '
    with open(file_path, 'w', errors='ignore') as file:
        file.write(docstr_code)

def issue_api_key(config):
    """
    This function generates a new API key for the given user.

    Arguments:
    config: dict, A dictionary containing the user's configuration details.
        - access_token: str, The user's access token.
        - username: str, The user's username.

    Returns:
    None, Prints the new API key to the console.

    Raises:
    Exception, If the API key generation fails. The error message will be printed to the console.

    """
    "\n    This function generates a new API key for the given user.\n\n    Arguments:\n    config: dict, A dictionary containing the user's configuration details.\n        - access_token: str, The user's access token.\n        - username: str, The user's username.\n\n    Returns:\n    None, Prints the new API key to the console.\n\n    Raises:\n    Exception, If the API key generation fails. The error message will be printed to the console.\n\n    "
    "\n    This function generates a new API key for the given user.\n\n    Arguments:\n    config: A dictionary containing the user's configuration details.\n        - access_token: str, The user's access token.\n        - username: str, The user's username.\n\n    Returns:\n    None, prints the new API key to the console.\n\n    Raises:\n    Exception, If the API key generation fails. The error message will be printed to the console.\n    "
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
    This function is used to sign up a user with the provided configuration.

    Arguments:
    config: dict
        A dictionary containing the user's signup information.

    Returns:
    None

    Raises:
    Exception
        If the username or email already exists.
        If there's a general error during the sign up process.
    """
    "\n    This function is used to sign up a user with the provided configuration.\n\n    Arguments:\n    config: dict\n        A dictionary containing the user's signup information.\n\n    Returns:\n    None\n\n    Raises:\n    Exception\n        If the username or email already exists.\n        If there's a general error during the sign up process.\n    "
    '\ndef signup(config: dict) -> None:\n    '
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