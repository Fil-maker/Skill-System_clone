from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from api.services.auth import token_auth
from api.services.users import abort_if_user_not_found, only_for_current_user, get_user, delete_user, \
    update_user, get_countries_count, get_regions_count, create_user


class UserResource(Resource):
    @abort_if_user_not_found
    def get(self, user_id):
        return jsonify({"success": True, "user": get_user(user_id)})

    @abort_if_user_not_found
    @token_auth.login_required
    @only_for_current_user
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
        args = parser.parse_args(strict=True)  # Вызовет ошибку, если запрос
        # будет содержать поля, которых нет в парсере
        try:
            update_user(user_id, args)
        except KeyError as e:
            abort(400, success=False, message=str(e))
        return jsonify({'success': True})


class UserListResource(Resource):
    def get(self):
        return jsonify({"success": True, "users": get_user()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("first_name", required=True)
        parser.add_argument("last_name", required=True)
        parser.add_argument("country", required=True, type=int, choices=range(1, get_countries_count() + 1))
        parser.add_argument("region", type=int, choices=range(1, get_regions_count() + 1))
        parser.add_argument("email", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("photo", type=FileStorage)

        args = parser.parse_args(strict=True)
        try:
            token, expires = create_user(args)
        except KeyError as e:
            abort(400, success=False, message=str(e))
        else:
            return jsonify({"success": True, "authToken": {"token": token,
                                                           "expires": expires}})
