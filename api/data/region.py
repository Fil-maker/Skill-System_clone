from sqlalchemy import Column, Integer, String, ForeignKey

from api.data.db_session import SqlAlchemyBase


class Region(SqlAlchemyBase):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    name = Column(String, nullable=False)
    code = Column(String(2), nullable=False, unique=True)
