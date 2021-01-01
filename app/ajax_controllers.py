from flask import jsonify, Blueprint

from app.services.events import change_event_participant_role, add_user_to_event, exclude_user_from_event

ajax = Blueprint("ajax", __name__)


@ajax.route("/participants/promote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def promote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role + 1)
    return jsonify(data)


@ajax.route("/participants/demote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def demote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role - 1)
    return jsonify(data)


@ajax.route("/participants/assign/<int:event_id>/<int:user_id>", methods=["POST"])
def assign_user_to_event(event_id, user_id):
    data = add_user_to_event(event_id, user_id)
    return jsonify(data)


@ajax.route("/participants/exclude/<int:event_id>/<int:user_id>", methods=["POST"])
def exclude_user_from_event_(event_id, user_id):
    data = exclude_user_from_event(event_id, user_id)
    return jsonify(data)


@ajax.route("/forms/assign/<int:event_id>/<int:form_id>", methods=["POST"])
def assign_form_to_event(event_id, form_id):
    data = {'success': True}
    return jsonify(data)


@ajax.route("/forms/delete/<int:event_id>/<int:form_id>", methods=["POST"])
def delete_form_from_event(event_id, form_id):
    data = {'success': True}
    return jsonify(data)
