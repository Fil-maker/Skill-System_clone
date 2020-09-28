import os

import requests
from flask import session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/users"


def redirect_if_authorized(func):
    def new_func(*args, **kwargs):
        token = session.get("token", None)
        print(token)
        if token:
            return redirect("/")
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    return new_func


def confirm_token(token) -> bool:
    r = requests.post(f"{api_url}/confirm/{token}")
    return r.json()["success"]


def register_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            form.password.render_kw["class"] = "input-str form-control is-invalid"
            form.password_again.render_kw["class"] = "input-str form-control is-invalid"
            form.password_again.errors.append("Passwords don't match")
            return False
        if not is_password_secure(form.password.data):
            form.password.render_kw["class"] = "input-str form-control is-invalid"
            form.password.errors.append("Insecure password")
            return False

        data = register_user(form.email.data, form.first_name.data, form.last_name.data,
                             form.country.data, form.region.data, form.password.data,
                             form.photo.data)
        if data["success"]:
            return True
        if f"email {form.email.data} " in data.get("message", ""):
            form.email.render_kw["class"] = "input-str form-control is-invalid"
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
    return data


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
