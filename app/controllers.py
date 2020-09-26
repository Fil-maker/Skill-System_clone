import os

import requests

from app import app

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api"


@app.route("/confirm/<token>")
def confirm(token):
    r = requests.post(f"{api_url}/confirm/{token}")
    return r.json()
