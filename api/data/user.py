import datetime
import secrets

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from api.data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    reg_date = Column(DateTime, nullable=False)
    password = Column(String, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

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

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id
