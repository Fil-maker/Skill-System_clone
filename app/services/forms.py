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


def delete_form(form_id):
    response = requests.delete(f"{api_url}/{form_id}", auth=HTTPTokenAuth())
    data = response.json()
    return data


def update_form_from_form(form_id, form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = update_form(form_id, form.title.data, form.content.data, form.day.data, form.role.data)

        if data["success"]:
            return True
        if "Incorrect day format" == data.get("message", ""):
            form.day.render_kw["class"] = "form-control is-invalid"
            form.day.errors.append(data["message"])
        elif "Form that is used cannot be changed" == data.get("message", ""):
            form.title.render_kw["class"] = "form-control is-invalid"
            form.content.render_kw["class"] = "form-control is-invalid"
            form.day.render_kw["class"] = "form-control is-invalid"
            form.errors.render_kw["class"] = "form-control is-invalid"
            form.errors.errors.append(data["message"])
    return False


def update_form(form_id, title=None, content=None, day=None, role=None):
    params = {}
    if title:
        params["title"] = title
    if content:
        params["content"] = content
    if day:
        params["day"] = day
    if role:
        params["role"] = role

    response = requests.put(f"{api_url}/{form_id}", params, auth=HTTPTokenAuth())
    data = response.json()
    return data


def get_form_signatory(event_id, form_id):
    response = requests.get(f"{events_api_url}/{event_id}/forms/{form_id}/signatory", auth=HTTPTokenAuth())
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
    response = requests.post(f"{events_api_url}/{event_id}/forms/{form_id}/signatory", {
        "pin": pin
    }, auth=HTTPTokenAuth())

    return response.json()
