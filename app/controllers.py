from flask import render_template
from werkzeug.utils import redirect

from app import app
from app.forms.login import LoginForm
from app.forms.password import PasswordForm
from app.forms.pin import PinForm
from app.forms.register import RegisterForm
from app.services.users import confirm_token, register_from_form, redirect_if_authorized, \
    login_from_form, user_logout, redirect_if_unauthorized


@app.route("/confirm/<token>")
def confirm(token):
    return "ok" if confirm_token(token) else "not ok"


@app.route("/register", methods=["GET", "POST"])
@redirect_if_authorized
def register():
    form = RegisterForm()
    if register_from_form(form):
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@redirect_if_authorized
def login():
    form = LoginForm()
    if login_from_form(form):
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
@redirect_if_unauthorized
def logout():
    user_logout()
    return redirect("/login")


@app.route("/pin", methods=["GET", "POST"])
@redirect_if_unauthorized
def pin():
    form = PinForm()
    return render_template("pin.html", form=form)


@app.route("/password", methods=["GET", "POST"])
@redirect_if_unauthorized
def password():
    form = PasswordForm()
    return render_template("password.html", form=form)
