from sqlalchemy import Column, Integer, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from api.data.db_session import db


class FormMustSignAssociation(db.Model, SerializerMixin):
    __tablename__ = "form_must_sign_association"
    form_to_event_id = Column(Integer, ForeignKey("form_to_event_association.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    form_to_event = orm.relation("FormToEventAssociation", foreign_keys=[form_to_event_id])
    user = orm.relation("User", foreign_keys=[user_id])

    def to_dict_form(self, *args, **kwargs):
        if "only" in kwargs:
            return super(FormMustSignAssociation, self).to_dict(*args, **kwargs)
        return {
            "form": self.form_to_event.to_dict()
        }

    def to_dict_user(self, *args, **kwargs):
        if "only" in kwargs:
            return super(FormMustSignAssociation, self).to_dict(*args, **kwargs)
        return {
            "user": self.user.to_dict()
        }