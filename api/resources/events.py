import datetime

from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.auth import token_auth
from api.services.events import abort_if_event_not_found, get_event, delete_event, update_event, \
    create_event, get_event_participants, add_users_to_event, exclude_users_from_event, \
    only_for_admin_and_chief_expert, get_event_forms, add_form_to_event, remove_form_from_event, get_unassigned_users, \
    change_event_participant_role, get_unassigned_forms
from api.services.users import only_for_admin


class EventResource(Resource):
    @abort_if_event_not_found
    def get(self, event_id):
        return jsonify({"success": True, "event": get_event(event_id)})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
    def delete(self, event_id):
        delete_event(event_id)
        return jsonify({"success": True})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
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
        return jsonify({
            "success": True,
            "participants": get_event_participants(event_id),
            "unassigned": get_unassigned_users(event_id)
        })

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
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
    @only_for_admin_and_chief_expert
    def put(self, event_id):
        parser = RequestParser()
        parser.add_argument("user_id", required=True, type=int)
        parser.add_argument("role", required=True, type=int)
        args = parser.parse_args()
        try:
            change_event_participant_role(event_id, **args)
        except (KeyError, ValueError) as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
    def delete(self, event_id):
        parser = RequestParser()
        parser.add_argument("users", required=True, type=int, action="append")
        args = parser.parse_args()
        try:
            exclude_users_from_event(event_id, **args)
        except KeyError as e:
            abort(400, success=False, message=str(e))
        return jsonify({"success": True})


class EventFormListResource(Resource):
    @abort_if_event_not_found
    def get(self, event_id):
        return jsonify({
            "success": True,
            "forms": get_event_forms(event_id),
            "unassigned": get_unassigned_forms(event_id)
        })

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
    def post(self, event_id):
        parser = RequestParser()
        parser.add_argument("form_id", required=True, type=int)
        args = parser.parse_args()
        try:
            add_form_to_event(event_id, args["form_id"])
        except KeyError as e:
            abort(404, success=False, message=str(e))
        except ValueError as e:
            abort(400, success=False, message=str(e))
        return jsonify({"success": True})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
    def delete(self, event_id):
        parser = RequestParser()
        parser.add_argument("form_id", required=True, type=int)
        args = parser.parse_args()
        try:
            remove_form_from_event(event_id, args["form_id"])
        except KeyError as e:
            abort(404, success=False, message=str(e))
        return jsonify({"success": True})
