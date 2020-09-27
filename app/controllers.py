import os

from flask import render_template
import requests

from app import app
from app.forms.login import LoginForm
from app.forms.password import PasswordForm
from app.forms.pin import PinForm
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


@app.route("/pin", methods=['GET', 'POST'])
def pin():
    form = PinForm()
    return render_template('pin.html', form=form)


@app.route("/password", methods=['GET', 'POST'])
def password():
    form = PasswordForm()
    return render_template('password.html', form=form)
