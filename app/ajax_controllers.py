from flask import jsonify, Blueprint

from app.services.events import change_event_participant_role, add_user_to_event, exclude_user_from_event, \
    add_form_to_event, remove_form_from_event, delete_event
from app.services.forms import delete_form
from app.services.users import delete_user

ajax = Blueprint("ajax", __name__)


@ajax.route("/participants/promote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def promote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role + 1)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/participants/demote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def demote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role - 1)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/participants/assign/<int:event_id>/<int:user_id>", methods=["POST"])
def assign_user_to_event(event_id, user_id):
    data = add_user_to_event(event_id, user_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/participants/exclude/<int:event_id>/<int:user_id>", methods=["POST"])
def delete_user_from_event_(event_id, user_id):
    data = exclude_user_from_event(event_id, user_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/forms/assign/<int:event_id>/<int:form_id>", methods=["POST"])
def assign_form_to_event(event_id, form_id):
    data = add_form_to_event(event_id, form_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/forms/delete/<int:event_id>/<int:form_id>", methods=["POST"])
def delete_form_from_event(event_id, form_id):
    data = remove_form_from_event(event_id, form_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/delete/user/<int:user_id>", methods=["POST"])
def delete_user_(user_id):
    data = delete_user(user_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/delete/event/<int:event_id>", methods=["POST"])
def delete_event_(event_id):
    data = delete_event(event_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/delete/form/<int:form_id>", methods=["POST"])
def delete_form_(form_id):
    data = delete_form(form_id)
    return jsonify(data), 200 if data["success"] else 400
