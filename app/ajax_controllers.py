from flask import jsonify, Blueprint

from app.services.events import change_event_participant_role, add_user_to_event, exclude_user_from_event

ajax = Blueprint("ajax", __name__)


@ajax.route("/promote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def promote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role + 1)
    return jsonify(data)


@ajax.route("/demote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def demote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role - 1)
    return jsonify(data)


@ajax.route("/assign/<int:event_id>/<int:user_id>", methods=["POST"])
def assign_user_to_event(event_id, user_id):
    data = add_user_to_event(event_id, user_id)
    return jsonify(data)


@ajax.route("/exclude/<int:event_id>/<int:user_id>", methods=["POST"])
def exclude_user_from_event_(event_id, user_id):
    data = exclude_user_from_event(event_id, user_id)
    return jsonify(data)
