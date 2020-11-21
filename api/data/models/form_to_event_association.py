from sqlalchemy import ForeignKey, Integer, Column, Table, orm

from api.data.db_session import db

forms_signatures = Table("forms_signatures", db.metadata,
                         Column("form_to_event_association_id", Integer, ForeignKey("form_to_event_association.id")),
                         Column("user_id", Integer, ForeignKey("users.id")))


class FormToEventAssociation(db.Model):
    __tablename__ = "form_to_event_association"
    id = Column(Integer, primary_key=True, autoincrement=True)
    form_id = Column(Integer, ForeignKey("forms.id"), index=True)
    event_id = Column(Integer, ForeignKey("events.id"), index=True)

    form = orm.relation("Form", foreign_keys=[form_id])
    event = orm.relation("Event", back_populates="forms")

    signatory = orm.relation("User", secondary=forms_signatures, back_populates="signed_forms")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(FormToEventAssociation, self).to_dict(*args, **kwargs)
        ans = super(FormToEventAssociation, self).to_dict(*args, **kwargs, only=["id", "event_id", "form"])
        ans["signatory"] = [user.id for user in self.signatory]
