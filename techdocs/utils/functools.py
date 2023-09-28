import json
import requests

BASE_URL = "http://localhost:8000"



def get_access_token(data, return_refresh_token=False):
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




def request_inference(config, code_block, max_retries=1):

    if max_retries == 0:
        return None

    url = BASE_URL+"/api/inference"
    headers={"accept":"application/json", "Authorization": f"Bearer {config['access_token']}"}
    code_input = code_block
    response = requests.post(url=url, headers=headers, params={'code_block':code_input, 'api_key':config['api_key']})
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
    

    

    
