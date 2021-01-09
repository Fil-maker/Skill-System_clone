import os
from enum import Enum

import requests
from flask import session, g
from flask_wtf import FlaskForm
from requests.auth import AuthBase
from werkzeug.exceptions import abort
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


class Roles(Enum):
    NO_ROLE = 0
    ADMIN = 1


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


def only_for_admin(func):
    def new_func(*args, **kwargs):
        if Roles(g.current_user["role"]) != Roles.ADMIN:
            abort(404)
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    return new_func


def only_for_admin_and_chief_expert(func):
    def new_func(*args, **kwargs):
        if not (Roles(g.current_user["role"]) == Roles.ADMIN or
                g.current_event["chief_expert"] and g.current_event["chief_expert"]["id"] == g.current_user["id"]):
            abort(404)
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    return new_func


def get_user(user_id=None):
    if user_id is not None:
        response = requests.get(f"{api_url}/{user_id}")
        data = response.json()
        if data["success"]:
            return data["user"]
    else:
        response = requests.get(api_url)
        data = response.json()
        if data["success"]:
            return data["users"]
    return None


def get_events(user_id):
    response = requests.get(f"{api_url}/{user_id}/events", auth=HTTPTokenAuth())
    data = response.json()
    if data["success"]:
        return data["events"]


def get_forms(user_id):
    response = requests.get(f"{api_url}/{user_id}/forms", auth=HTTPTokenAuth())
    data = response.json()
    if data["success"]:
        return data


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
                             form.photo_base64.data)
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


def edit_profile_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = update_user(g.current_user["id"],
                           form.first_name.data, form.last_name.data, form.country.data,
                           form.region.data, form.photo_base64.data, form.about.data)
        return data["success"]
    return False


def update_user(user_id, first_name=None, last_name=None, country=None, region=None, photo=None, about=None):
    params = {}
    if first_name:
        params["first_name"] = first_name
    if last_name:
        params["last_name"] = last_name
    if country:
        params["country"] = country
    if region:
        params["region"] = region
    if photo:
        params["photo"] = photo
    if about:
        params["about"] = about

    response = requests.put(f"{api_url}/{user_id}", params, auth=HTTPTokenAuth())
    data = response.json()
    return data


def delete_user(user_id):
    response = requests.delete(f"{api_url}/{user_id}", auth=HTTPTokenAuth())
    data = response.json()
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
    response = requests.patch(f"{api_url}/{g.current_user['id']}",
                              auth=HTTPTokenAuth(),
                              data={
                                  "old_password": old_password,
                                  "new_password": new_password
                              })
    data = response.json()
    if data["success"]:
        session["token"] = data["authToken"]["token"]
    return data


def set_pin_from_form(form: FlaskForm):
    if form.validate_on_submit():
        pin = form.pin.data
        if not (pin.isdigit() and len(pin) == 4):
            form.pin.render_kw["class"] = "form-control is-invalid"
            form.pin.errors.append("PIN must be 4 digits")
            return False
        data = set_pin(pin)
        if data["success"]:
            return True
        form.pin.render_kw["class"] = "form-control is-invalid"
        form.pin.errors.append(data.get("message", ""))
    return False


def set_pin(pin):
    response = requests.post(f"{api_url}/{g.current_user['id']}/pin",
                             auth=HTTPTokenAuth(),
                             data={"pin": pin})
    data = response.json()
    return data


def reset_pin():
    response = requests.delete(f"{api_url}/{g.current_user['id']}/pin", auth=HTTPTokenAuth())
    data = response.json()
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
