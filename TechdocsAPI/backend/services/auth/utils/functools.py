import requests
from typing import Any, Dict
import json

def post_request(url: str, data: Dict[str, Any], headers: Dict[str, str]=None):
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.status_code