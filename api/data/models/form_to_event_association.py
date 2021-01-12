from sqlalchemy import ForeignKey, Integer, Column, orm, Date, Boolean

from api.data.db_session import db
from api.data.mixins.iso8601_serializer_mixin import ISO8601SerializerMixin
from api.data.models.user_to_event_association import EventRoles, UserToEventAssociation


class FormToEventAssociation(db.Model, ISO8601SerializerMixin):
    __tablename__ = "form_to_event_association"
    id = Column(Integer, primary_key=True, autoincrement=True)
    form_id = Column(Integer, ForeignKey("forms.id"), index=True)
    event_id = Column(Integer, ForeignKey("events.id"), index=True)
    date = Column(Date)
    hidden = Column(Boolean, default=False)

    form = orm.relation("Form", foreign_keys=[form_id])
    event = orm.relation("Event", foreign_keys=[event_id])

    signatory = orm.relation("FormSignatoryAssociation", back_populates="form_to_event", lazy="dynamic")
    must_sign = orm.relation("FormMustSignAssociation", back_populates="form_to_event", lazy="dynamic")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(FormToEventAssociation, self).to_dict(*args, **kwargs)
        ans = super(FormToEventAssociation, self).to_dict(*args, **kwargs, only=["event_id"])
        ans["form"] = self.form.to_dict()
        ans["date"] = self.serialize_date(self.date)
        ans["signed"] = self.signatory.count()
        ans["must_sign"] = [item.user_id for item in self.must_sign]
        ans["signatory"] = [item.user_id for item in self.signatory]
        return ans
