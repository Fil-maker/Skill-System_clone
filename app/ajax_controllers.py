from flask import jsonify, Blueprint

ajax = Blueprint("ajax", __name__)


@ajax.route("/promote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def promote_user_in_event(event_id, user_id, role):
    return jsonify({
        "data": f"{user_id} promoted in {event_id} with role {role}+1"
    })


@ajax.route("/demote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def demote_user_in_event(event_id, user_id, role):
    return jsonify({
        "data": f"{user_id} demoted in {event_id} with role {role}-1"
    })
