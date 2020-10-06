from sqlalchemy import Column, Integer, Date, String, orm, Table, ForeignKey

from api.data.db_session import db

association_table = Table("user_to_event", db.metadata,
                          Column("user", Integer, ForeignKey("users.id")),
                          Column("event", Integer, ForeignKey("events.id"))
                          )


class Event(db.Model):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)

    start_date = Column(Date, nullable=False)
    main_stage_date = Column(Date, nullable=False)
    final_stage_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)

    photo_url = Column(String, nullable=True)

    participants = orm.relation("User", secondary="user_to_event")
