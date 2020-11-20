from flask import jsonify

from app import app


@app.route("/ajax/promote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def promote_user_in_event(event_id, user_id, role):
    print(1)
    return jsonify({
        'data': f"{user_id} promoted in {event_id} with role {role}+1"
    })


@app.route("/ajax/demote/<int:event_id>/<int:user_id>/<int:role>", methods=["POST"])
def demote_user_in_event(event_id, user_id, role):
    print(2)
    return jsonify({'data': f"{user_id} demoted in {event_id} with role {role}-1"})
