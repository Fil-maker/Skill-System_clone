from flask import jsonify, send_file
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.data.models.user_to_event_association import EventRoles
from api.services.auth import token_auth
from api.services.events import abort_if_event_not_found, only_for_admin_and_chief_expert
from api.services.forms import abort_if_form_not_found, delete_form, get_form, update_form, \
    create_form, get_form_signatory, sign_form, abort_if_event_form_not_found, get_event_form
from api.services.users import only_for_admin
from api.services.word import render_form_template


class FormsResource(Resource):
    @abort_if_form_not_found
    def get(self, form_id):
        return jsonify({"success": True, "form": get_form(form_id=form_id)})

    @abort_if_form_not_found
    @token_auth.login_required
    @only_for_admin
    def delete(self, form_id):
        delete_form(form_id)
        return jsonify({"success": True})

    @abort_if_form_not_found
    @token_auth.login_required
    @only_for_admin
    def put(self, form_id):
        parser = RequestParser()
        parser.add_argument("title")
        parser.add_argument("content")
        parser.add_argument("day")
        args = parser.parse_args(strict=True)
        try:
            form = update_form(form_id, **args)
        except (KeyError, ValueError) as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True, "form": form})


class FormListResource(Resource):
    def get(self):
        return jsonify({"success": True, "forms": get_form()})

    @token_auth.login_required
    @only_for_admin
    def post(self):
        parser = RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("content", required=True)
        parser.add_argument("day", required=True)
        parser.add_argument("role", required=True, type=int, choices=[EventRoles.COMPETITOR.value,
                                                                      EventRoles.EXPERT.value])
        args = parser.parse_args(strict=True)
        try:
            form = create_form(**args)
        except (ValueError, KeyError) as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True, "form": form})


class EventFormResource(Resource):
    @abort_if_event_form_not_found
    def get(self, event_id, form_id):
        return jsonify({"success": True, "eventForm": get_event_form(event_id, form_id)})


class FormSignatoryResource(Resource):
    @abort_if_event_form_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
    def get(self, event_id, form_id):
        return jsonify({"success": True, "signatory": get_form_signatory(event_id, form_id)})

    @abort_if_event_form_not_found
    @token_auth.login_required
    def post(self, event_id, form_id):
        parser = RequestParser()
        parser.add_argument("pin", required=True, type=int)
        args = parser.parse_args()
        try:
            sign_form(event_id, form_id, **args)
        except KeyError as e:
            abort(403, success=False)
        except ValueError as e:
            print(e)
            abort(403, success=False, message=str(e))
        else:
            return jsonify({"success": True})


class FormDocumentResource(Resource):
    @abort_if_event_form_not_found
    @token_auth.login_required
    @only_for_admin_and_chief_expert
    def get(self, event_id, form_id):
        file = render_form_template(event_id, form_id)
        return send_file(file, as_attachment=True, attachment_filename="form.docx")
