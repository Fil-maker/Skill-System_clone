import datetime

from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.auth import token_auth
from api.services.events import abort_if_event_not_found, get_event, delete_event, update_event, \
    create_event, get_event_participants, add_users_to_event, exclude_users_from_event
from api.services.users import only_for_admin


class EventResource(Resource):
    @abort_if_event_not_found
    def get(self, event_id):
        return jsonify({"success": True, "event": get_event(event_id)})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin
    def delete(self, event_id):
        delete_event(event_id)
        return jsonify({"success": True})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin
    def put(self, event_id):
        parser = RequestParser()
        parser.add_argument("title")
        parser.add_argument("start_date", type=datetime.date.fromisoformat)
        parser.add_argument("main_stage_date", type=datetime.date.fromisoformat)
        parser.add_argument("final_stage_date", type=datetime.date.fromisoformat)
        parser.add_argument("finish_date", type=datetime.date.fromisoformat)
        parser.add_argument("photo")
        args = parser.parse_args(strict=True)

        try:
            event = update_event(event_id, **args)
        except (KeyError, ValueError) as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True, "event": event})


class EventListResource(Resource):
    def get(self):
        return jsonify({"success": True, "events": get_event()})

    @token_auth.login_required
    @only_for_admin
    def post(self):
        parser = RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("start_date", required=True, type=datetime.date.fromisoformat)
        parser.add_argument("main_stage_date", required=True, type=datetime.date.fromisoformat)
        parser.add_argument("final_stage_date", required=True, type=datetime.date.fromisoformat)
        parser.add_argument("finish_date", required=True, type=datetime.date.fromisoformat)
        parser.add_argument("photo")

        args = parser.parse_args(strict=True)
        try:
            event = create_event(**args)
        except (KeyError, ValueError) as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True, "event": event})


class EventParticipantResource(Resource):
    @abort_if_event_not_found
    def get(self, event_id):
        return jsonify({"success": True, "participants": get_event_participants(event_id)})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin
    def post(self, event_id):
        parser = RequestParser()
        parser.add_argument("users", required=True, type=dict, action="append", location="json")
        args = parser.parse_args()
        try:
            add_users_to_event(event_id, **args)
        except (KeyError, ValueError) as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin
    def delete(self, event_id):
        parser = RequestParser()
        parser.add_argument("users", required=True, type=int, action="append")
        args = parser.parse_args()
        try:
            exclude_users_from_event(event_id, **args)
        except KeyError as e:
            abort(400, success=False, message=str(e))
        return jsonify({"success": True})
