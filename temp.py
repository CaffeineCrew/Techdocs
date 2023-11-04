import requests
import json


def post_request(url, data, headers=None):
    data = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    return response.status_code, response.json()

email_body_params = {
    "username": "mayo",
    "verify_link": "verification_link"
}
details = {
        "recipient": ["mayureshagashe2002@outlook.com", "alfatrion123@gmail.com"],
        "subject": "Welcome to Techdocs:[Account Verification]",
        "template_name": "email_verification.html",
        "template_kwargs": email_body_params
    }
print(post_request("https://email-server-five.vercel.app/api/send", details))