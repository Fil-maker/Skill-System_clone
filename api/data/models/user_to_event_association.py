from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from sqlalchemy import orm

from api.data.db_session import db


class EventRoles(Enum):
    COMPETITOR = 0
    EXPERT = 1
    CHIEF_EXPERT = 2


class UserToEventAssociation(db.Model):
    __tablename__ = "user_to_event_association"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    role = Column(SmallInteger, nullable=False, default=EventRoles.COMPETITOR.value)

    participant = orm.relation("User", back_populates="events")
    event = orm.relation("Event", back_populates="participants")

    def to_dict_participant(self):
        return {
            "user": self.participant.to_dict(),
            "role": self.role
        }

    def to_dict_event(self):
        return {
            "event": self.event.to_dict(),
            "role": self.role
        }
