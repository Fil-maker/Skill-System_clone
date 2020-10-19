import datetime
import os
import secrets
from enum import Enum

import jwt
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, orm, DateTime, Boolean, SmallInteger, \
    Text
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from api.data.db_session import db
from api.data.models.form import forms_signatures


class Roles(Enum):
    NO_ROLE = 0
    ADMIN = 1


class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    password = Column(String, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    photo_url = Column(String, nullable=True)
    about = Column(Text, nullable=True, default="")

    role = Column(SmallInteger, nullable=False, default=Roles.NO_ROLE.value)
    pin = Column(String, nullable=True)

    country = orm.relation("Country", foreign_keys=[country_id])
    region = orm.relation("Region", foreign_keys=[region_id])

    events = orm.relation("UserToEventAssociation", back_populates="participant", lazy="dynamic")
    signed_forms = orm.relation("Form", secondary=forms_signatures, back_populates="signatory")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_pin(self, pin):
        self.pin = generate_password_hash(pin)

    def check_pin(self, pin):
        return check_password_hash(self.pin, pin)

    token = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    token_expiration = sqlalchemy.Column(sqlalchemy.DateTime)

    def get_token(self, expires_in=3600 * 24):
        now = datetime.datetime.now()
        if self.token and self.token_expiration > now + datetime.timedelta(seconds=60):
            # Если токен действительный, возвращаем его
            return self.token
        # Иначе, генерируем новый и устанавливаем срок истечения (по умолчанию через 24 часа)
        self.token = secrets.token_urlsafe(32)
        self.token_expiration = now + datetime.timedelta(seconds=expires_in)
        return self.token

    def revoke_token(self):
        # Отзыв токена (Время истечения изменяется на текущее - 1 секунда)
        self.token_expiration = datetime.datetime.now() - datetime.timedelta(seconds=1)

    def get_confirmation_token(self, expires_in=3600 * 24):
        return jwt.encode({
            "confirm": self.id,
            "exp": datetime.datetime.now() + datetime.timedelta(seconds=expires_in)},
            os.environ.get("API_SECRET"), algorithm="HS256").decode("utf-8")

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(User, self).to_dict(*args, **kwargs)
        ans = super(User, self).to_dict(*args, **kwargs,
                                        only=["id", "email", "first_name", "last_name", "country",
                                              "region", "creation_date", "confirmed", "about", "role"])
        if self.photo_url is not None:
            photos = {
                "initial": f"{os.environ.get('S3_BUCKET_URL')}/users/init/{self.photo_url}",
                "128": f"{os.environ.get('S3_BUCKET_URL')}/users/128/{self.photo_url}",
                "256": f"{os.environ.get('S3_BUCKET_URL')}/users/256/{self.photo_url}",
                "512": f"{os.environ.get('S3_BUCKET_URL')}/users/512/{self.photo_url}",
            }
            ans["photos"] = photos
        ans["is_pin_set"] = self.pin is not None
        return ans

    def __hash__(self):
        return hash(self.id)
