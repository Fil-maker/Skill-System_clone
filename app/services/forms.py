import os
import requests
api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/forms"


def get_form(form_id=None):
    if form_id is not None:
        response = requests.get(f"{api_url}/{form_id}")
        data = response.json()
        if data["success"]:
            return data["form"]
    else:
        response = requests.get(api_url)
        data = response.json()
        if data["success"]:
            return data["forms"]
    return None
