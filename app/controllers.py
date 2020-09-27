import os

from flask import render_template
import requests

from app import app
from app.forms.login import LoginForm
from app.forms.register import RegisterForm

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api"


@app.route("/confirm/<token>")
def confirm(token):
    r = requests.post(f"{api_url}/confirm/{token}")
    return r.json()


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
