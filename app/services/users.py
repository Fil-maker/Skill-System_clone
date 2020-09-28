import os

import requests
from flask import session, g
from flask_wtf import FlaskForm
from requests.auth import AuthBase
from werkzeug.utils import redirect

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/users"


class HTTPTokenAuth(AuthBase):
    def __init__(self, token=None):
        if token is None:
            token = session.get("token", "")
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, "token", None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


def redirect_if_authorized(func):
    def new_func(*args, **kwargs):
        token = session.get("token", None)
        if token:
            return redirect("/")
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    return new_func


def redirect_if_unauthorized(func):
    def new_func(*args, **kwargs):
        token = session.get("token", None)
        if token:
            return func(*args, **kwargs)
        return redirect("/login")

    new_func.__name__ = func.__name__
    return new_func


def confirm_token(token) -> bool:
    r = requests.post(f"{api_url}/confirm/{token}")
    return r.json()["success"]


def register_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            form.password.render_kw["class"] = "form-control is-invalid"
            form.password_again.render_kw["class"] = "form-control is-invalid"
            form.password_again.errors.append("Passwords don't match")
            return False
        if not is_password_secure(form.password.data):
            form.password.render_kw["class"] = "form-control is-invalid"
            form.password.errors.append("Insecure password")
            return False

        data = register_user(form.email.data, form.first_name.data, form.last_name.data,
                             form.country.data, form.region.data, form.password.data,
                             form.photo.data)
        if data["success"]:
            return True
        if f"email {form.email.data} " in data.get("message", ""):
            form.email.render_kw["class"] = "form-control is-invalid"
            form.email.errors.append(data["message"])
    return False


def register_user(email, first_name, last_name, country, region, password, photo):
    response = requests.post(api_url, {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "country": country,
        "region": region,
        "password": password,
        "photo": photo
    })

    data = response.json()
    if data["success"]:
        session["token"] = data["authToken"]["token"]
        g.current_user = data["user"]
    return data


def login_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = login_user(form.email.data, form.password.data)
        if data["success"]:
            return True
        form.email.render_kw["class"] = "form-control is-invalid"
        form.password.render_kw["class"] = "form-control is-invalid"
        form.password.errors.append("Invalid email or password")
    return False


def login_user(email, password):
    response = requests.post(f"{api_url}/login", auth=(email, password))
    data = response.json()
    if data["success"]:
        session["token"] = data["authToken"]["token"]
        g.current_user = data["user"]
    return data


def logout():
    response = requests.post(f"{api_url}/logout", auth=HTTPTokenAuth())
    if response.json()["success"]:
        session.pop("token", None)
        g.current_user = None
        return True
    return False


def change_password_from_form(form: FlaskForm):
    if form.validate_on_submit():
        if form.new_password.data != form.password_again.data:
            form.new_password.render_kw["class"] = "form-control is-invalid"
            form.password_again.render_kw["class"] = "form-control is-invalid"
            form.password_again.errors.append("Passwords don't match")
            return False
        if not is_password_secure(form.new_password.data):
            form.new_password.render_kw["class"] = "form-control is-invalid"
            form.new_password.errors.append("Insecure password")
            return False
        data = change_password(form.cur_password.data, form.new_password.data)
        if data["success"]:
            return True
        if "Invalid" in data.get("message", ""):
            form.cur_password.render_kw["class"] = "form-control is-invalid"
            form.cur_password.errors.append("Invalid password")
        elif "different" in data.get("message", ""):
            form.new_password.render_kw["class"] = "form-control is-invalid"
            form.new_password.errors.append(data.get("message", ""))
    return False


def change_password(old_password, new_password):
    response = requests.post(f"{api_url}/{g.current_user['id']}/change-password",
                             auth=HTTPTokenAuth(),
                             data={
                                 "old_password": old_password,
                                 "new_password": new_password
                             })
    data = response.json()
    if data["success"]:
        session["token"] = data["authToken"]["token"]
    print(data)
    return data


def get_myself():
    response = requests.get(f"{api_url}/get-myself", auth=HTTPTokenAuth())
    data = response.json()
    if data["success"]:
        return data["user"]
    return None


def is_password_secure(password: str) -> bool:
    return not (len(password) < 8 or
                password.isdigit() or
                password.isalpha() or
                password.islower() or
                password.isupper()) and password.isalnum()


_COUNTRIES = None
_REGIONS = None
_COUNTRIES_COUNT = None
_REGIONS_COUNT = None
_RU_ID = None


def get_countries_list():
    global _COUNTRIES, _COUNTRIES_COUNT
    if _COUNTRIES is None:
        r = requests.get(f"{api_url}/countries")
        _COUNTRIES = r.json()["countries"]
        _COUNTRIES_COUNT = len(_COUNTRIES)
    return _COUNTRIES


def get_countries_count():
    global _COUNTRIES_COUNT
    if _COUNTRIES_COUNT is None:
        get_countries_list()
    return _COUNTRIES_COUNT


def get_regions_list():
    global _REGIONS, _REGIONS_COUNT
    if _REGIONS is None:
        r = requests.get(f"{api_url}/regions")
        _REGIONS = r.json()["regions"]
        _REGIONS_COUNT = len(_REGIONS)
    return _REGIONS


def get_regions_count():
    global _REGIONS_COUNT
    if _REGIONS_COUNT is None:
        get_regions_list()
    return _REGIONS_COUNT


def get_ru_id():
    global _RU_ID, _COUNTRIES
    if _RU_ID is None:
        if _COUNTRIES is None:
            get_countries_list()
        for country in _COUNTRIES:
            if "Russian Federation" in country["name"]:
                _RU_ID = country["id"]
                break
    return _RU_ID
