import datetime

from sqlalchemy import Column, Integer, ForeignKey, orm, DateTime

from api.data.db_session import db
from api.data.mixins.iso8601_serializer_mixin import ISO8601SerializerMixin


class FormSignatoryAssociation(db.Model, ISO8601SerializerMixin):
    __tablename__ = "form_signatory_association"
    form_to_event_id = Column(Integer, ForeignKey("form_to_event_association.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    sign_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    form_to_event = orm.relation("FormToEventAssociation", foreign_keys=[form_to_event_id])
    user = orm.relation("User", foreign_keys=[user_id])

    def to_dict_form(self, *args, **kwargs):
        if "only" in kwargs:
            return super(FormSignatoryAssociation, self).to_dict(*args, **kwargs)
        return {
            "form": self.form_to_event.to_dict(),
            "sign_date": self.serialize_datetime(self.sign_date)
        }

    def to_dict_user(self, *args, **kwargs):
        if "only" in kwargs:
            return super(FormSignatoryAssociation, self).to_dict(*args, **kwargs)
        return {
            "user": self.user.to_dict(),
            "sign_date": self.serialize_datetime(self.sign_date)
        }
