import os

import requests
from flask import g
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort

from app.services.users import HTTPTokenAuth

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/events"


def load_event_to_g_or_abort(func):
    def new_func(event_id, *args, **kwargs):
        event = get_event(event_id)
        if event is None:
            abort(404)
        else:
            g.current_event = event
        return func(event_id, *args, **kwargs)

    new_func.__name__ = func.__name__
    return new_func


def get_event(event_id=None):
    if event_id is not None:
        response = requests.get(f"{api_url}/{event_id}")
        data = response.json()
        if data["success"]:
            return data["event"]
    else:
        response = requests.get(api_url)
        data = response.json()
        if data["success"]:
            return data["events"]
    return None


def create_event_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = create_event(form.title.data, form.start_date.data, form.main_stage_date.data,
                            form.final_stage_date.data, form.finish_date.data, form.photo_base64.data)
        if data["success"]:
            return True
        if "Dates are inconsistent" == data.get("message", ""):
            form.start_date.render_kw["class"] = "form-control is-invalid"
            form.main_stage_date.render_kw["class"] = "form-control is-invalid"
            form.final_stage_date.render_kw["class"] = "form-control is-invalid"
            form.finish_date.render_kw["class"] = "form-control is-invalid"
            form.finish_date.errors.append(data["message"])
        elif "already finished" in data.get("message", ""):
            form.finish_date.render_kw["class"] = "form-control is-invalid"
            form.finish_date.errors.append(data["message"])
    return False


def create_event(title, start_date, main_stage_date, final_stage_date, finish_date, photo):
    response = requests.post(api_url, {
        "title": title,
        "start_date": start_date,
        "main_stage_date": main_stage_date,
        "final_stage_date": final_stage_date,
        "finish_date": finish_date,
        "photo": photo
    }, auth=HTTPTokenAuth())

    return response.json()


def edit_event_information_from_form(event_id, form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = update_event(event_id, title=form.title.data)
        return data["success"]
    return False


def edit_event_dates_from_form(event_id, form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = update_event(event_id, start_date=form.start_date.data,
                            main_stage_date=form.main_stage_date.data,
                            final_stage_date=form.final_stage_date.data,
                            finish_date=form.finish_date.data)

        if data["success"]:
            return True
        if "Dates are inconsistent" == data.get("message", ""):
            form.start_date.render_kw["class"] = "form-control is-invalid"
            form.main_stage_date.render_kw["class"] = "form-control is-invalid"
            form.final_stage_date.render_kw["class"] = "form-control is-invalid"
            form.finish_date.render_kw["class"] = "form-control is-invalid"
            form.finish_date.errors.append(data["message"])
        elif "already finished" in data.get("message", ""):
            form.finish_date.render_kw["class"] = "form-control is-invalid"
            form.finish_date.errors.append(data["message"])
    return False


def update_event(event_id, title=None, start_date=None, main_stage_date=None, final_stage_date=None,
                 finish_date=None, photo=None):
    params = {}
    if title:
        params["title"] = title
    if start_date:
        params["start_date"] = start_date
    if main_stage_date:
        params["main_stage_date"] = main_stage_date
    if final_stage_date:
        params["final_stage_date"] = final_stage_date
    if finish_date:
        params["finish_date"] = finish_date
    if photo:
        params["photo"] = photo

    response = requests.put(f"{api_url}/{event_id}", params, auth=HTTPTokenAuth())
    data = response.json()
    return data


def delete_event(event_id):
    response = requests.delete(f"{api_url}/{event_id}", auth=HTTPTokenAuth())
    data = response.json()
    return data


def get_event_forms(event_id):
    if event_id is not None:
        response = requests.get(f"{api_url}/{event_id}/forms")
        data = response.json()
        if data["success"]:
            return data


def get_event_participants(event_id):
    response = requests.get(f"{api_url}/{event_id}/participants")
    data = response.json()
    if data["success"]:
        return data


def add_user_to_event(event_id, user_id):
    response = requests.post(f"{api_url}/{event_id}/participants", json={
        "users": [{"id": user_id}]
    }, auth=HTTPTokenAuth())
    return response.json()


def change_event_participant_role(event_id, user_id, role):
    response = requests.put(f"{api_url}/{event_id}/participants", {
        "user_id": user_id,
        "role": role
    }, auth=HTTPTokenAuth())
    return response.json()


def exclude_user_from_event(event_id, user_id):
    response = requests.delete(f"{api_url}/{event_id}/participants", params={
        "users": user_id
    }, auth=HTTPTokenAuth())
    return response.json()


def add_form_to_event(event_id, form_id):
    response = requests.post(f"{api_url}/{event_id}/forms", {"form_id": form_id}, auth=HTTPTokenAuth())
    return response.json()


def remove_form_from_event(event_id, form_id):
    response = requests.delete(f"{api_url}/{event_id}/forms", params={"form_id": form_id}, auth=HTTPTokenAuth())
    return response.json()
