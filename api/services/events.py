import datetime

from flask import g
from flask_restful import abort
from sqlalchemy import desc

from api.data.db_session import create_session
from api.data.models import Event, User, UserToEventAssociation
from api.data.models.form import Form
from api.data.models.user import Roles
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


def only_for_admin_and_chief_expert(resource="event"):
    def decorator(func):
        def new_func(self, id_):
            with create_session() as session:
                if resource == "event":
                    event_id = id_
                elif resource == "form":
                    event_id = session.query(Form).get(id_).event_id
                else:
                    raise TypeError
                association = session.query(UserToEventAssociation).filter(
                    UserToEventAssociation.user_id == g.current_user.id,
                    UserToEventAssociation.event_id == event_id).first()
                if Roles(g.current_user.role) == Roles.ADMIN:
                    pass
                elif association is not None and EventRoles(association.role) == EventRoles.CHIEF_EXPERT:
                    pass
                else:
                    abort(403, success=False)
                return func(self, id_)

        return new_func
    return decorator


def get_event(event_id=None):
    with create_session() as session:
        if event_id is not None:
            return session.query(Event).get(event_id).to_dict()
        today = datetime.date.today()
        ongoing_events = session.query(Event).filter(Event.start_date <= today,
                                                     today <= Event.finish_date).all()
        future_events = session.query(Event).filter(Event.start_date > today).order_by(
            Event.start_date).all()
        past_events = session.query(Event).filter(Event.finish_date < today).order_by(
            desc(Event.finish_date)).all()
        return [item.to_dict() for item in ongoing_events + future_events + past_events]


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

            if not (start_date < main_stage_date < final_stage_date < finish_date):
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
                    role = EventRoles(user_json.get("role", EventRoles.COMPETITOR.value))
                except ValueError:
                    raise ValueError(f"Role can be {EventRoles.COMPETITOR.value} (competitor), "
                                     f"{EventRoles.EXPERT.value} (expert) or "
                                     f"{EventRoles.CHIEF_EXPERT.value} (chief expert)")
                if role == EventRoles.CHIEF_EXPERT:
                    if event.chief_expert_id is None:
                        event.chief_expert_id = user.id
                    else:
                        raise ValueError("Chief expert is already assigned")
                association = UserToEventAssociation(user_id=user.id, role=role.value)
                event.participants.append(association)


def exclude_users_from_event(event_id, users):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        for user_id in users:
            user = session.query(User).get(int(user_id))
            if not user:
                raise KeyError(f"User {user_id} not found")
            if user in event.participants:
                if user.id == event.chief_expert_id:
                    event.chief_expert_id = None
                event.participants.remove(user)


def get_dates_from_c_format(start_date: datetime.date, main_stage_date: datetime.date,
                            final_stage_date: datetime.date, finish_date: datetime.date):
    """
    :return: A dictionary where the key is a c-format date and the value is a regular date
    """
    dates = {}
    for i in range((main_stage_date - start_date).days, 0, -1):
        dates[f"C-{i}"] = main_stage_date - datetime.timedelta(days=i)
    for i in range((final_stage_date - main_stage_date).days):
        dates[f"C{i + 1}"] = main_stage_date + datetime.timedelta(days=i)
    for i in range((finish_date - final_stage_date).days + 1):
        dates[f"C+{i + 1}"] = final_stage_date + datetime.timedelta(days=i)
    return dates


def get_c_format_from_dates(start_date: datetime.date, main_stage_date: datetime.date,
                            final_stage_date: datetime.date, finish_date: datetime.date):
    """
    :return: A dictionary where the key is a regular date and the value is a c-format date
    """
    dates = get_dates_from_c_format(start_date, main_stage_date, final_stage_date, finish_date)
    return {value: key for key, value in dates.items()}
