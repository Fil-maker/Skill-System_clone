from sqlalchemy import Column, Integer, String, Text, SmallInteger, orm
from sqlalchemy_serializer import SerializerMixin

from api.data.db_session import db


class Form(db.Model, SerializerMixin):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    day = Column(String, nullable=False)
    role = Column(SmallInteger, nullable=False)

    events = orm.relation("FormToEventAssociation", back_populates="form", lazy="dynamic")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Form, self).to_dict(*args, **kwargs)
        ans = super(Form, self).to_dict(*args, **kwargs, only=["id", "title", "content", "day", "role"])
        return ans
