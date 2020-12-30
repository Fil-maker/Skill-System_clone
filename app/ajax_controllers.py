from flask import jsonify, Blueprint

from app.services.events import change_event_participant_role

ajax = Blueprint("ajax", __name__)


@ajax.route("/promote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def promote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role + 1)
    return jsonify(data)


@ajax.route("/demote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def demote_user_in_event(event_id, user_id, role):
    data = change_event_participant_role(event_id, user_id, role - 1)
    return jsonify(data)
