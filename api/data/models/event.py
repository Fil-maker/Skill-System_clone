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
        ans = super(Event, self).to_dict(*args, **kwargs, only=["id", "title"])
        if self.photo_url is not None:
            photos = {
                "initial": f"{os.environ.get('S3_BUCKET_URL')}/events/init/{self.photo_url}",
                "128": f"{os.environ.get('S3_BUCKET_URL')}/events/128/{self.photo_url}",
                "256": f"{os.environ.get('S3_BUCKET_URL')}/events/256/{self.photo_url}",
                "512": f"{os.environ.get('S3_BUCKET_URL')}/events/512/{self.photo_url}",
            }
            ans["photos"] = photos
        ans["participants"] = [participant.participant.id for participant in self.participants]

        from api.services.events import get_dates_from_c_format, get_c_format_from_dates
        dates = get_dates_from_c_format(self.start_date, self.main_stage_date, self.final_stage_date,
                                        self.finish_date)
        c_format = get_c_format_from_dates(self.start_date, self.main_stage_date,
                                           self.final_stage_date, self.finish_date)
        c_minus_n = c_format[self.start_date]
        c_n = c_format[self.final_stage_date - datetime.timedelta(days=1)]
        c_plus_n = c_format[self.finish_date]
        ans["dates"] = {
            c_minus_n: dates[c_minus_n],
            "C-1": dates["C-1"],
            "C1": dates["C1"],
            c_n: dates[c_n],
            "C+1": dates["C+1"],
            c_plus_n: dates[c_plus_n]
        }

        ans["forms"] = [form.id for form in self.forms]
        return ans
