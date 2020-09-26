from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin

from api.data.db_session import db


class Country(db.Model, SerializerMixin):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    alpha_code = Column(String(2), nullable=False, unique=True)
    numeric_code = Column(String(3), nullable=False, unique=True)
