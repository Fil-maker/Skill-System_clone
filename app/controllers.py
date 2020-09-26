import os

from flask import render_template
import requests

from app import app
from app.forms.register import RegisterForm

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api"


@app.route("/confirm/<token>")
def confirm(token):
    r = requests.post(f"{api_url}/confirm/{token}")
    return r.json()

  
@app.route("/")
def test():
    form = RegisterForm()
    return render_template('register.html', form=form)
