from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.auth import token_auth
from api.services.users import abort_if_user_not_found, only_for_current_user, get_user, delete_user, \
    update_user, get_countries_count, get_regions_count, create_user, change_password, set_pin, \
    reset_pin, get_events, only_for_current_user_or_admin, get_signed_forms, get_unsigned_forms, get_events_to_assign, \
    only_for_admin


class UserResource(Resource):
    @abort_if_user_not_found
    def get(self, user_id):
        return jsonify({"success": True, "user": get_user(user_id)})

    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user_or_admin
    def delete(self, user_id):
        delete_user(user_id)
        return jsonify({"success": True})

    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user
    def put(self, user_id):
        parser = RequestParser()
        parser.add_argument("first_name")
        parser.add_argument("last_name")
        parser.add_argument("country", type=int)
        parser.add_argument("region", type=int)
        parser.add_argument("photo")
        parser.add_argument("about")
        args = parser.parse_args(strict=True)  # Вызовет ошибку, если запрос
        # будет содержать поля, которых нет в парсере
        try:
            user = update_user(user_id, **args)
        except (KeyError, ValueError) as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True, "user": user})

    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user
    def patch(self, user_id):  # Password change
        parser = RequestParser()
        parser.add_argument("old_password", required=True)
        parser.add_argument("new_password", required=True)
        args = parser.parse_args(strict=True)
        token, expires = change_password(user_id, **args)
        return jsonify({"success": True, "authToken": {"token": token,
                                                       "expires": expires}})


class UserListResource(Resource):
    def get(self):
        return jsonify({"success": True, "users": get_user()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("email", required=True)
        parser.add_argument("first_name", required=True)
        parser.add_argument("last_name", required=True)
        parser.add_argument("country", required=True, type=int,
                            choices=range(1, get_countries_count() + 1))
        parser.add_argument("region", type=int, choices=range(1, get_regions_count() + 1))
        parser.add_argument("password", required=True)
        parser.add_argument("photo")

        args = parser.parse_args(strict=True)
        try:
            user, token, expires = create_user(**args)
        except KeyError as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True, "user": user,
                            "authToken": {"token": token,
                                          "expires": expires}})


class UserPinResource(Resource):
    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user
    def post(self, user_id):
        parser = RequestParser()
        parser.add_argument("pin", required=True)
        args = parser.parse_args(strict=True)
        return jsonify({"success": set_pin(user_id, **args)})

    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user
    def delete(self, user_id):
        return jsonify({"success": reset_pin(user_id)})


class UsersEventListResource(Resource):
    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user
    def get(self, user_id):
        return jsonify({"success": True, "events": get_events(user_id)})


class UsersAssignToEventResource(Resource):
    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_admin
    def get(self, user_id):
        return jsonify({"success": True, "events": get_events_to_assign(user_id)})


class UsersFormListResource(Resource):
    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user
    def get(self, user_id):
        return jsonify({
            "success": True,
            "signed": get_signed_forms(user_id),
            "must_sign": get_unsigned_forms(user_id)
        })
