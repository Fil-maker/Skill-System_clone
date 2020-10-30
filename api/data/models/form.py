from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, orm, Table, SmallInteger
from sqlalchemy_serializer import SerializerMixin

from api.data.db_session import db

forms_signatures = Table("forms_signatures", db.metadata,
                         Column("form_id", Integer, ForeignKey("forms.id")),
                         Column("user_id", Integer, ForeignKey("users.id"))
                         )


class Form(db.Model, SerializerMixin):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    role = Column(SmallInteger, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = orm.relation("Event", foreign_keys=[event_id])
    signatory = orm.relation("User", secondary=forms_signatures, back_populates="signed_forms")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Form, self).to_dict(*args, **kwargs)
        ans = super(Form, self).to_dict(*args, **kwargs, only=["id", "title", "content", "event_id"])
        ans["signatory"] = [user.id for user in self.signatory]
        event = self.event
        from api.services.events import get_c_format_from_dates
        ans["day"] = get_c_format_from_dates(event.start_date, event.main_stage_date,
                                             event.final_stage_date, event.finish_date)[self.date]
        return ans
