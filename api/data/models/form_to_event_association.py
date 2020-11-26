from sqlalchemy import ForeignKey, Integer, Column, orm, Date

from api.data.db_session import db
from api.data.mixins.iso8601_serializer_mixin import ISO8601SerializerMixin
from api.data.models.user_to_event_association import EventRoles


class FormToEventAssociation(db.Model, ISO8601SerializerMixin):
    __tablename__ = "form_to_event_association"
    id = Column(Integer, primary_key=True, autoincrement=True)
    form_id = Column(Integer, ForeignKey("forms.id"), index=True)
    event_id = Column(Integer, ForeignKey("events.id"), index=True)
    date = Column(Date)

    form = orm.relation("Form", foreign_keys=[form_id])
    event = orm.relation("Event", foreign_keys=[event_id])

    signatory = orm.relation("FormSignatoryAssociation", back_populates="form_to_event", lazy="dynamic")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(FormToEventAssociation, self).to_dict(*args, **kwargs)
        ans = super(FormToEventAssociation, self).to_dict(*args, **kwargs, only=["id", "event_id"])
        ans["form"] = self.form.to_dict()
        ans["date"] = self.serialize_date(self.date)
        ans["signed"] = self.signatory.count()
        ans["must_sign"] = len(list(filter(lambda x: x.role == EventRoles.CHIEF_EXPERT.value or
                                                     x.role == self.form.role, self.event.participants)))
        ans["signatory"] = [sign.user_id for sign in self.signatory]
        return ans
