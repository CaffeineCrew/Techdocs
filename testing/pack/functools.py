import json
import requests
BASE_URL = 'https://caffeinecrew-techdocs.hf.space'

def get_access_token(data, return_refresh_token=False):
    """Authenticates and returns the access token.

    Args:
        data: dict. User login credentials.

    Returns:
        str. The access token.
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
    """Request for inference from an external model.

    Args:
        config: Config. Configuration dictionary with model credentials,
                api key, and access token.
        code_block: str. Code block for which inference is requested.
        max_retries: int, optional. Number of retries to be made in case
                 of failure. Defaults to 1.

    Returns:
        str: Docstring generated from the model.
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
    """insert a single record or iterable of records to the database.

        Args:
            db_name (str): name of the database
            coll_name (str): name of the collection
            data (dict): data to be inserted

        Returns:
            An instance of class: pymongo.results.InsertOneResult or 
            pymongo.results.InsertManyResult
        """
    with open(file_path, 'w', errors='ignore') as file:
        file.write(docstr_code)

def issue_api_key(config):
    """Issues an API key for a valid user

    Args:
        config (dict): Config dictionary containing `username` and `access_token`
        of the user.

    Raises:
        Exception: If API key generation fails.
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
    """Sends a request to the server to create a new user account.

    Args:
        config (dict): A dictionary containing the following keys:
            - 'username': The username of the new user.
            - 'email': The email address of the new user.
            - 'password': The password of the new user.

    Raises:
        Exception: If the request fails or the status code is not 200.
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