import datetime

from flask_restful import abort

from api.data.db_session import create_session
from api.data.models import Event, User, UserToEventAssociation
from api.data.models.user_to_event_association import EventRoles
from api.services.images import delete_photo, generate_photo_filename, save_photo


def abort_if_event_not_found(func):
    def new_func(self, event_id):
        with create_session() as session:
            event = session.query(Event).get(event_id)
            if not event:
                abort(404, success=False, message=f"Event {event_id} not found")
            return func(self, event_id)

    return new_func


def get_event(event_id=None):
    with create_session() as session:
        if event_id is not None:
            return session.query(Event).get(event_id).to_dict()
        return [item.to_dict() for item in session.query(Event).all()]


def delete_event(event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        delete_photo("events", event.photo_url)
        session.delete(event)


def create_event(title, start_date, main_stage_date, final_stage_date, finish_date, photo=None):
    with create_session() as session:
        if not (start_date < main_stage_date < final_stage_date < finish_date):
            raise ValueError("Dates are inconsistent")
        if finish_date <= datetime.date.today():
            raise ValueError("Event is already finished")

        event = Event(
            title=title,
            start_date=start_date,
            main_stage_date=main_stage_date,
            final_stage_date=final_stage_date,
            finish_date=finish_date
        )
        session.add(event)
        session.commit()
        if photo:
            set_photo(event.id, photo)
        return event.to_dict()


def update_event(event_id, title=None, start_date=None, main_stage_date=None, final_stage_date=None,
                 finish_date=None, photo=None):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        if title:
            event.title = title
        if any((start_date, main_stage_date, final_stage_date, finish_date)):
            start_date = event.start_date if start_date is None else start_date
            main_stage_date = event.main_stage_date if main_stage_date is None else main_stage_date
            final_stage_date = event.final_stage_date if final_stage_date is None else final_stage_date
            finish_date = event.finish_date if finish_date is None else finish_date

            if not(start_date < main_stage_date < final_stage_date < finish_date):
                raise ValueError("Dates are inconsistent")
            if finish_date <= datetime.date.today():
                raise ValueError("Event is already finished")

            event.start_date = start_date
            event.main_stage_date = main_stage_date
            event.final_stage_date = final_stage_date
            event.finish_date = finish_date

        if photo:
            set_photo(event_id, photo)
        return event.to_dict()


def set_photo(event_id, photo):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        if event.photo_url is not None:
            delete_photo("events", event.photo_url)
        filename = generate_photo_filename(event_id)
        save_photo(photo, "events", filename)
        event.photo_url = filename


def get_event_participants(event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        return [participant.to_dict_participant() for participant in event.participants]


def add_users_to_event(event_id, users):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        for user_json in users:
            try:
                user = session.query(User).get(int(user_json["id"]))
            except KeyError:
                raise KeyError("You must specify user id")
            if not user:
                raise KeyError(f"User {user_json['id']} not found")
            if user not in map(lambda x: x.participant, event.participants):
                try:
                    association = UserToEventAssociation(user_id=user.id,
                                                         role=EventRoles(user_json.get("role",
                                                                                       EventRoles.COMPETITOR.value)).value)
                except ValueError:
                    raise ValueError(f"Role can be {EventRoles.COMPETITOR.value} (competitor), "
                                     f"{EventRoles.EXPERT.value} (expert) or "
                                     f"{EventRoles.CHIEF_EXPERT.value} (chief expert)")
                event.participants.append(association)


def exclude_users_from_event(event_id, users):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        for user_id in users:
            user = session.query(User).get(int(user_id))
            if not user:
                raise KeyError(f"User {user_id} not found")
            if user in event.participants:
                event.participants.remove(user)
