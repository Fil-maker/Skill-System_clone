import json

from flask import jsonify, g, request
from flask_restful import abort
from werkzeug.exceptions import HTTPException

from api import app
from api.services.auth import basic_auth, token_auth
from api.services.users import confirm_email, get_countries_list, get_regions_list, change_password, \
    set_pin, reset_pin


@app.errorhandler(HTTPException)
def error(e):
    response = e.get_response()
    params = {
        "success": False,
    }
    try:
        for key, value in e.data.items():
            params[key] = value
    except AttributeError:
        pass
    response.data = json.dumps(params)
    response.content_type = "application/json"
    return response


@app.route("/api/users/login", methods=["POST"])
@basic_auth.login_required
# Путь получает в заголовках запроса логин и пароль пользователя (декоратор @basic.auth.login_required)
# и, если данные верны, возвращает токен. Чтобы защитить маршруты API с помощью токенов, необходимо
# добавить декоратор @token_auth.login_required
def get_token():
    token = g.current_user.get_token()
    g.db_session.commit()
    return jsonify({"success": True, "user": g.current_user.to_dict(),
                    "authToken": {"token": token,
                                  "expires": str(g.current_user.token_expiration)}})


@app.route("/api/users/logout", methods=["POST"])
@token_auth.login_required
# Отзыв токена
def revoke_token():
    g.current_user.revoke_token()
    g.db_session.commit()
    g.current_user = None
    g.db_session = None
    return jsonify({"success": True})


@app.route("/api/users/confirm/<token>", methods=["POST"])
def confirm(token):
    success = confirm_email(token)
    return jsonify({"success": success})


@app.route("/api/users/countries")
def get_countries():
    return jsonify({"success": True,
                    "countries": get_countries_list()})


@app.route("/api/users/regions")
def get_regions():
    return jsonify({"success": True,
                    "regions": get_regions_list()})


@app.route("/api/users/<int:user_id>/change-password", methods=["POST"])
@token_auth.login_required
def change_password_(user_id):
    if g.current_user.id != user_id:
        abort(403)
    if "old_password" not in request.form:
        abort(400, message="You must enter your old password")
    if "new_password" not in request.form:
        abort(400, message="You must enter your new password")
    token, expires = change_password(user_id, request.form["old_password"],
                                     request.form["new_password"])
    return jsonify({"success": True, "authToken": {"token": token,
                                                   "expires": expires}})


@app.route("/api/users/get-myself")
@token_auth.login_required
def get_myself():
    return jsonify({"success": True, "user": g.current_user.to_dict()})


@app.route("/api/users/<int:user_id>/set-pin", methods=["POST"])
@token_auth.login_required
def set_pin_(user_id):
    if "pin" not in request.form:
        abort(400, "You must enter pin")
    return jsonify({"success": set_pin(user_id, request.form["pin"])})


@app.route("/api/users/<int:user_id>/reset-pin", methods=["POST"])
@token_auth.login_required
def reset_pin_(user_id):
    return jsonify({"success": reset_pin(user_id)})
