import os

import jwt
from flask import g, render_template
from flask_restful import abort

from api.data.db_session import create_session
from api.data.models import Country, Region, User
from api.services.email import send_email


def abort_if_user_not_found(func):
    def new_func(self, user_id):
        with create_session() as session:
            user = session.query(User).get(user_id)
            if not user:
                abort(404, message=f"User {user_id} not found")
            return func(self, user_id)

    return new_func


def only_for_current_user(func):
    def new_func(self, user_id):
        if user_id != g.current_user.id:
            abort(403)
        return func(self, user_id)

    return new_func


def get_user(user_id=None):
    with create_session() as session:
        if user_id is not None:
            return session.query(User).get(user_id).to_dict()
        return [item.to_dict() for item in session.query(User).all()]


def delete_user(user_id):
    with create_session() as session:
        session.delete(session.query(User).get(user_id))


def update_user(user_id, args):
    with create_session() as session:
        user = session.query(User).get(user_id)
        if args["country"]:
            if args["country"] == get_ru_id() and user.country_id != get_ru_id():
                if args["region"]:
                    user.country_id = args["country"]
                    user.region_id = args["region"]
                else:
                    raise KeyError("You must specify the region for this country")
            else:
                user.country_id = args["country"]
        if args["first_name"]:
            user.first_name = args["first_name"]
        if args["last_name"]:
            user.last_name = args["last_name"]
        return user.to_dict()


def create_user(args):
    with create_session() as session:
        if session.query(User).filter(User.email == args["email"]).first() is not None:
            abort(400, message=f"User with email {args['email']} already exists")
        user = User(
            email=args["email"],
            first_name=args["first_name"],
            last_name=args["last_name"],
            country_id=args["country"],
        )
        if args["country"] == get_ru_id():
            if args["region"]:
                user.region_id = args["region"]
            else:
                raise KeyError("You must specify the region for this country")
        else:
            user.country_id = args["country"]
        user.set_password(args["password"])
        # TODO: Сохранение фотографий в Amazon S3
        token = user.get_token()
        expires = user.token_expiration
        session.add(user)
        session.commit()
        send_confirmation_token(user)
        return user.to_dict(), token, expires


def send_confirmation_token(user):
    token = user.get_confirmation_token()
    url = f"http://{os.environ.get('APP_HOST')}:{os.environ.get('APP_PORT')}/confirm/{token}"
    send_email("Registration confirmation",
               sender=os.environ.get("MAIL_USERNAME"),
               recipients=[user.email],
               text_body=render_template("email/confirmation.txt", user=user, url=url),
               html_body=render_template("email/confirmation.html", user=user, url=url))


def confirm_email(token):
    try:
        user_id = jwt.decode(token, os.environ.get("API_SECRET"), algorithms=["HS256"])["confirm"]
    except jwt.exceptions.DecodeError:
        return False
    with create_session() as session:
        session.query(User).get(user_id).confirmed = True
    return True


def change_password(user_id, old_password, new_password):
    with create_session() as session:
        user = session.query(User).get(user_id)
        if not user.check_password(old_password):
            abort(400, message="Invalid old password")
        if user.check_password(new_password):
            abort(400, message="New password must be different from the old")
        user.set_password(new_password)
        user.revoke_token()
        token = user.get_token()
        expires = user.token_expiration
    return token, expires


_COUNTRIES = None
_REGIONS = None
_COUNTRIES_COUNT = None
_REGIONS_COUNT = None
_RU_ID = None


def get_countries_list():
    global _COUNTRIES, _COUNTRIES_COUNT
    if _COUNTRIES is None:
        with create_session() as session:
            _COUNTRIES = [item.to_dict() for item in session.query(Country).all()]
            _COUNTRIES_COUNT = len(_COUNTRIES)
    return _COUNTRIES


def get_countries_count():
    global _COUNTRIES_COUNT
    if _COUNTRIES_COUNT is None:
        get_countries_list()
    return _COUNTRIES_COUNT


def get_regions_list():
    global _REGIONS, _REGIONS_COUNT
    if _REGIONS is None:
        with create_session() as session:
            _REGIONS = [item.to_dict() for item in session.query(Region).all()]
            _REGIONS_COUNT = len(_REGIONS)
    return _REGIONS


def get_regions_count():
    global _REGIONS_COUNT
    if _REGIONS_COUNT is None:
        get_regions_list()
    return _REGIONS_COUNT


def get_ru_id():
    global _RU_ID
    if _RU_ID is None:
        with create_session() as session:
            _RU_ID = session.query(Country).filter(Country.name.like("%Russian Federation%")).first().id
    return _RU_ID
