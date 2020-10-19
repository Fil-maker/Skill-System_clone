import os

from sqlalchemy import Column, Integer, Date, String, orm
from sqlalchemy_serializer import SerializerMixin

from api.data.db_session import db


class Event(db.Model, SerializerMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)
    main_stage_date = Column(Date, nullable=False)
    final_stage_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)

    photo_url = Column(String, nullable=True)

    participants = orm.relation("UserToEventAssociation", back_populates="event", lazy="dynamic")
    forms = orm.relation("Form", back_populates="event")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Event, self).to_dict(*args, **kwargs)
        ans = super(Event, self).to_dict(*args, **kwargs,
                                         only=["id", "title", "start_date", "main_stage_date",
                                               "final_stage_date", "finish_date"])
        if self.photo_url is not None:
            photos = {
                "initial": f"{os.environ.get('S3_BUCKET_URL')}/events/init/{self.photo_url}",
                "128": f"{os.environ.get('S3_BUCKET_URL')}/events/128/{self.photo_url}",
                "256": f"{os.environ.get('S3_BUCKET_URL')}/events/256/{self.photo_url}",
                "512": f"{os.environ.get('S3_BUCKET_URL')}/events/512/{self.photo_url}",
            }
            ans["photos"] = photos
        ans["participants"] = [participant.participant.id for participant in self.participants]
        ans["forms"] = [form.id for form in self.forms]
        return ans
