from sqlalchemy import Column, Integer, String

from api.data.db_session import SqlAlchemyBase


class Country(SqlAlchemyBase):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    alpha_code = Column(String(2), nullable=False, unique=True)
    numeric_code = Column(String(3), nullable=False, unique=True)
