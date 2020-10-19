from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from api.data.models.user_to_event_association import EventRoles
from api.services.auth import token_auth
from api.services.events import abort_if_event_not_found, only_for_admin_and_chief_expert
from api.services.forms import abort_if_form_not_found, delete_form, get_form, update_form, \
    create_form


class FormsResource(Resource):
    @abort_if_form_not_found
    def get(self, form_id):
        return jsonify({"success": True, "form": get_form(form_id=form_id)})

    @abort_if_form_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert("form")
    def delete(self, form_id):
        delete_form(form_id)
        return jsonify({"success": True})

    @abort_if_form_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert("form")
    def put(self, form_id):
        parser = RequestParser()
        parser.add_argument("title")
        parser.add_argument("content")
        parser.add_argument("date")  # TODO 1: проебразование даты из обычного формата в  /С[-+]?[1-9]+/
        args = parser.parse_args(strict=True)

        event = update_form(form_id, **args)
        return jsonify({"success": True, "event": event})


class FormListResource(Resource):
    @abort_if_event_not_found
    def get(self, event_id):
        return jsonify({"success": True, "forms": get_form(event_id=event_id)})

    @abort_if_event_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert("event")
    def post(self, event_id):
        parser = RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("content", required=True)
        parser.add_argument("date", required=True)  # TODO 1
        parser.add_argument("role", required=True, type=int, choices=[EventRoles.COMPETITOR.value,
                                                                      EventRoles.EXPERT.value])
        args = parser.parse_args(strict=True)

        form = create_form(**args, event_id=event_id)
        return jsonify({"success": True, "form": form})
