from flask import render_template, g, session
from werkzeug.utils import redirect

from app import app
from app.forms.editProfile import EditProfileForm
from app.forms.eventRegister import EventRegisterForm
from app.forms.login import LoginForm
from app.forms.password import PasswordForm
from app.forms.pin import PinForm
from app.forms.register import RegisterForm
from app.services.users import confirm_token, register_from_form, redirect_if_authorized, \
    login_from_form, logout, redirect_if_unauthorized, change_password_from_form, get_myself, \
    set_pin_from_form


@app.before_request
def before_request():
    if session.get("token", None):
        current_user = get_myself()
        if current_user is None:
            session.pop("token", None)
            return redirect("/")
        g.current_user = current_user


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
def logout_():
    logout()
    return redirect("/login")


@app.route("/pin", methods=["GET", "POST"])
@redirect_if_unauthorized
def pin():
    form = PinForm()
    if set_pin_from_form(form):
        return redirect("/")
    return render_template("pin.html", form=form)


@app.route("/change-password", methods=["GET", "POST"])
@redirect_if_unauthorized
def change_password_():
    form = PasswordForm()
    if change_password_from_form(form):
        return redirect("/")
    return render_template("password.html", form=form)


@app.route("/edit-profile", methods=['GET', 'POST'])
@redirect_if_unauthorized
def edit_profile():
    form = EditProfileForm()
    return render_template("editProfile.html", form=form)


@app.route("/profile", methods=["GET", "POST"])
@redirect_if_unauthorized
def profile():
    return render_template("userProfile.html")


@app.route("/create-event", methods=["GET", "POST"])
@redirect_if_unauthorized
def event_create():
    form = EventRegisterForm()
    return render_template("eventRegister.html", form=form)
