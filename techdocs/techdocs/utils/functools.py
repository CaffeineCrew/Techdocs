import json
import requests

BASE_URL = "https://caffeinecrew-techdocs.hf.space"
# BASE_URL = "http://127.0.0.1:8000"


def get_access_token(data, return_refresh_token=False):
    try:
        url = BASE_URL + "/auth/login"
        headers = {
            "accept": "application/json",
        }
        data = json.dumps(data)
        response = requests.post(url, data=data, headers=headers)
        access_token = response.json()['access_token']
        if return_refresh_token:
            refresh_token = response.json()['refresh_token']
            return access_token, refresh_token
        return access_token
    except Exception as e:
        if response.json() == "exception.InvalidCredentialsException()":  
            print("Please check your credentials")
        else:
            print("Please verify your email before logging in")
        return None


def request_inference(config, code_block, max_retries=1):

    if max_retries == 0:
        return None

    url = BASE_URL+"/api/inference"
    headers={"accept":"application/json", "Authorization": f"Bearer {config['access_token']}"}
    code_input = code_block
    response = requests.post(url=url, headers=headers, data=json.dumps({'code_block':code_input, 'api_key':config['api_key']}))
    if response.status_code == 200:
        return response.json()["docstr"]
    else:
        data = {
            "username":config['username'],
            "password":config['password']
        }
        print("Encountered error retrying...")
        config.update({"access_token":get_access_token(data)})
        
        return request_inference(config, code_block, max_retries=max_retries-1)
    

def update_file(file_path, docstr_code):
    with open(file_path, "w",errors='ignore') as file:
        file.write(docstr_code)


def issue_api_key(config):
    try:
        headers={"accept":"application/json", "Authorization": f"Bearer {config['access_token']}"}
        response = requests.put(url=BASE_URL + "/auth/regenerate_api_key", headers=headers, 
                                data=json.dumps({"username": config['username']})
                                )
        if (response.status_code!=200):
            raise Exception("API Key Generation Failed")
        print(f"$ API_KEY:{response.json()['api_key']}")
    except Exception as e:
        print(f"$ {e}")


def signup(config):
    try:
        headers={"accept":"application/json"}
        response = requests.post(url=BASE_URL + "/auth/signup", headers=headers, data=json.dumps(config))
        if (response.status_code==226):
            raise Exception("username or email already exists")
        elif (response.status_code!=200):
            raise Exception("Something went wrong, please try again later")
    
        print(response.json()["message"][0].replace('\\n','\n'), "Then issue a new `API_KEY` to continue")

    except Exception as e:
        print(e)
