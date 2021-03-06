import datetime
import os

from sqlalchemy import Column, Integer, Date, String, orm, ForeignKey, Boolean

from api.data.db_session import db
from api.data.mixins.iso8601_serializer_mixin import ISO8601SerializerMixin


class Event(db.Model, ISO8601SerializerMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)
    main_stage_date = Column(Date, nullable=False)
    final_stage_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)
    chief_expert_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hidden = Column(Boolean, default=False)
    photo_url = Column(String, nullable=True)

    participants = orm.relation("UserToEventAssociation", back_populates="event", lazy="dynamic")
    forms = orm.relation("FormToEventAssociation", back_populates="event", lazy="dynamic")
    chief_expert = orm.relation("User", foreign_keys=[chief_expert_id])

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Event, self).to_dict(*args, **kwargs)
        ans = super(Event, self).to_dict(*args, **kwargs, only=["id", "title"])
        if self.photo_url is not None:
            photos = {
                "initial": f"{os.environ.get('S3_BUCKET_URL')}/events/init/{self.photo_url}",
                "128": f"{os.environ.get('S3_BUCKET_URL')}/events/128/{self.photo_url}",
                "256": f"{os.environ.get('S3_BUCKET_URL')}/events/256/{self.photo_url}",
                "512": f"{os.environ.get('S3_BUCKET_URL')}/events/512/{self.photo_url}",
            }
            ans["photos"] = photos
        ans["participants"] = [participant.participant.id for participant in filter(lambda x: not x.participant.hidden,
                                                                                    self.participants)]
        ans["chief_expert"] = self.chief_expert.to_dict() if self.chief_expert is not None else None

        from api.services.events import get_dates_from_c_format, get_c_format_from_dates
        dates = get_dates_from_c_format(self.start_date, self.main_stage_date, self.final_stage_date,
                                        self.finish_date)
        c_format = get_c_format_from_dates(self.start_date, self.main_stage_date,
                                           self.final_stage_date, self.finish_date)
        c_minus_n = c_format[self.start_date]
        c_n = c_format[self.final_stage_date - datetime.timedelta(days=1)]
        c_plus_n = c_format[self.finish_date]
        ans["dates"] = {
            "C-N": {
                "name": c_minus_n,
                "date": self.serialize_date(dates[c_minus_n])
            },
            "C-1": self.serialize_date(dates["C-1"]),
            "C1": self.serialize_date(dates["C1"]),
            "CN": {
                "name": c_n,
                "date": self.serialize_date(dates[c_n])
            },
            "C+1": self.serialize_date(dates["C+1"]),
            "C+N": {
                "name": c_plus_n,
                "date": self.serialize_date(dates[c_plus_n])
            }
        }

        from api.data.models import FormToEventAssociation
        ans["forms"] = [form.id for form in self.forms.filter(FormToEventAssociation.hidden.is_(False))]
        return ans
