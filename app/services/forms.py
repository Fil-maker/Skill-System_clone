import os
import requests
from flask_wtf import FlaskForm

from app.services.users import HTTPTokenAuth

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/forms"
events_api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/events"


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


def create_form_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = create_form(form.title.data, form.day.data, form.content.data, form.role.data)
        if data["success"]:
            return True
        if "Incorrect day format" == data.get("message", ""):
            form.day.render_kw["class"] = "form-control is-invalid"
            form.day.errors.append(data["message"])
    return False


def create_form(title, day, content, role):
    response = requests.post(api_url, {
        "title": title,
        "day": day,
        "content": content,
        "role": role
    }, auth=HTTPTokenAuth())

    return response.json()


# TODO update_form() && update_form_from_form()


def get_form_signatory(event_id, form_id):
    response = requests.get(f"{events_api_url}/{event_id}/forms/{form_id}", auth=HTTPTokenAuth())
    data = response.json()
    if data["success"]:
        return data["signatory"]


def sign_form_from_form(event_id, form_id, form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = sign_form(event_id, form_id, form.pin.data)
        if data["success"]:
            return True
        else:
            form.pin.render_kw = "form-control is-invalid"
            form.pin.errors.append(data.get("message", ""))
    return False


def sign_form(event_id, form_id, pin):
    response = requests.post(f"{events_api_url}/{event_id}/forms/{form_id}", {
        "pin": pin
    }, auth=HTTPTokenAuth())

    return response.json()
