import datetime

from flask import g
from flask_restful import abort
from sqlalchemy import desc

from api.data.db_session import create_session
from api.data.models.event import Event
from api.data.models.form import Form
from api.data.models.form_must_sign_association import FormMustSignAssociation
from api.data.models.form_to_event_association import FormToEventAssociation
from api.data.models.user import Roles, User
from api.data.models.user_to_event_association import EventRoles, UserToEventAssociation
from api.services.images import delete_photo, generate_photo_filename, save_photo


def abort_if_event_not_found(func):
    def new_func(self, event_id):
        with create_session() as session:
            event = session.query(Event).filter(Event.id == event_id, Event.hidden.is_(False)).first()
            if not event:
                abort(404, success=False, message=f"Event {event_id} not found")
            return func(self, event_id)

    return new_func


def only_for_admin_and_chief_expert(func):
    def new_func(self, event_id, *args, **kwargs):
        with create_session() as session:
            association = session.query(UserToEventAssociation).filter(
                UserToEventAssociation.user_id == g.current_user.id,
                UserToEventAssociation.event_id == event_id).first()
            if Roles(g.current_user.role) == Roles.ADMIN:
                pass
            elif association is not None and EventRoles(association.role) == EventRoles.CHIEF_EXPERT:
                pass
            else:
                abort(403, success=False)
            return func(self, event_id, *args, **kwargs)

    return new_func


def get_event(event_id=None):
    with create_session() as session:
        if event_id is not None:
            return session.query(Event).get(event_id).to_dict()
        today = datetime.date.today()
        ongoing_events = session.query(Event).filter(Event.hidden.is_(False), Event.start_date <= today,
                                                     today <= Event.finish_date).all()
        future_events = session.query(Event).filter(Event.hidden.is_(False), Event.start_date > today) \
            .order_by(Event.start_date).all()
        past_events = session.query(Event).filter(Event.hidden.is_(False), Event.finish_date < today) \
            .order_by(desc(Event.finish_date)).all()
        return [item.to_dict() for item in ongoing_events + future_events + past_events]


def delete_event(event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        delete_photo("events", event.photo_url)
        event.hidden = True


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

            new_dates = get_dates_from_c_format(start_date, main_stage_date, final_stage_date, finish_date)
            for form in event.forms.filter(FormToEventAssociation.hidden.is_(False)):
                if form.day not in new_dates:
                    raise ValueError(f"Dates don't match form {form.id}")

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
        return {
            "chief-expert": event.chief_expert.to_dict() if event.chief_expert is not None else None,
            "experts": [
                expert.to_dict_participant() for expert in
                filter(lambda x: x.role == EventRoles.EXPERT.value and not x.participant.hidden, event.participants)
            ],
            "competitors": [
                competitor.to_dict_participant() for competitor in
                filter(lambda x: x.role == EventRoles.COMPETITOR.value and not x.participant.hidden, event.participants)
            ]
        }


def get_unassigned_users(event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        unassigned = sorted(list(filter(lambda x: x.id not in map(lambda x: x.user_id, event.participants),
                                        session.query(User).filter(User.confirmed, User.hidden.is_(False)).all())),
                            key=lambda x: x.creation_date)
        return [user.to_dict() for user in unassigned]


def add_users_to_event(event_id, users):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        for user_json in users:
            try:
                user = session.query(User).filter(User.id == int(user_json["id"]), User.hidden.is_(False)).first()
            except KeyError:
                raise KeyError("You must specify user id")
            if not user:
                raise KeyError(f"User {user_json['id']} not found")
            if not user.confirmed:
                raise ValueError(f"User {user.id} did not confirm his email")
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
                for form in event.forms:
                    if not form.hidden and (form.form.role == role.value or role == EventRoles.CHIEF_EXPERT):
                        form.must_sign.append(FormMustSignAssociation(user_id=user.id))


def change_event_participant_role(event_id, user_id, role):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        if event.start_date <= datetime.date.today():
            raise ValueError("You can't change the role after the event starts")

        user = session.query(User).filter(User.id == int(user_id), User.hidden.is_(False)).first()
        if not user:
            raise KeyError(f"User {user_id} not found")
        association = session.query(UserToEventAssociation) \
            .filter(UserToEventAssociation.user_id == user_id,
                    UserToEventAssociation.event_id == event_id).first()
        if association:
            try:
                role = EventRoles(role)
            except ValueError:
                raise ValueError(f"Role can be {EventRoles.COMPETITOR.value} (competitor), "
                                 f"{EventRoles.EXPERT.value} (expert) or "
                                 f"{EventRoles.CHIEF_EXPERT.value} (chief expert)")
            if association.role == role.value:
                raise ValueError(f"User is already a{'n' * int(role == EventRoles.EXPERT)} {role.name.lower()}")
            if role == EventRoles.CHIEF_EXPERT:
                if event.chief_expert_id is None:
                    event.chief_expert_id = user.id
                else:
                    raise ValueError("Chief expert is already assigned")
            if association.role == EventRoles.CHIEF_EXPERT.value:
                event.chief_expert_id = None
            for form in event.forms:
                if not form.hidden:
                    if form.form.role == role.value or role == EventRoles.CHIEF_EXPERT:
                        if association.role != EventRoles.CHIEF_EXPERT.value and form.form.role != association.role:
                            form.must_sign.append(FormMustSignAssociation(user_id=user.id))
                    else:
                        session.delete(form.must_sign.filter(FormMustSignAssociation.user_id == user_id).first())
            association.role = role.value


def exclude_users_from_event(event_id, users):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        for user_id in users:
            user = session.query(User).filter(User.id == int(user_id), User.hidden.is_(False)).first()
            if not user:
                raise KeyError(f"User {user_id} not found")
            association = session.query(UserToEventAssociation) \
                .filter(UserToEventAssociation.user_id == user_id,
                        UserToEventAssociation.event_id == event_id).first()
            if association:
                if user.id == event.chief_expert_id:
                    event.chief_expert_id = None
                for form in event.forms:
                    if not form.hidden and (form.form.role == association.role or
                                            association.role == EventRoles.CHIEF_EXPERT.value):
                        session.delete(form.must_sign.filter(FormMustSignAssociation.user_id == user_id).first())
                session.delete(association)


def get_event_forms(event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        return [form.to_dict() for form in event.forms.filter(FormToEventAssociation.hidden.is_(False))]


def get_unassigned_forms(event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        unassigned = list(filter(lambda x: x.id not in map(lambda x: x.form_id, event.forms),
                                 session.query(Form).filter(Form.hidden.is_(False)).all()))
        return [form.to_dict() for form in unassigned]


def add_form_to_event(event_id, form_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        form = session.query(Form).filter(Form.id == form_id, Form.hidden.is_(False)).first()
        if form is None:
            raise KeyError(f"Form {form_id} not found")
        if form_id in map(lambda x: x.form_id, event.forms.filter(FormToEventAssociation.hidden.is_(False))):
            raise ValueError(f"Form {form_id} is already added to event {event_id}")
        dates = get_dates_from_c_format(event.start_date, event.main_stage_date,
                                        event.final_stage_date, event.finish_date)
        if form.day not in dates:
            raise ValueError(f"Event {event_id} doesn't have day {form.day}")
        association = FormToEventAssociation(form_id=form_id, date=dates[form.day])
        event.forms.append(association)
        session.commit()
        for user in event.participants.filter(UserToEventAssociation.role == form.role):
            if not user.participant.hidden:
                association.must_sign.append(FormMustSignAssociation(user_id=user.participant.id))
        if event.chief_expert:
            association.must_sign.append(FormMustSignAssociation(user_id=event.chief_expert_id))


def remove_form_from_event(event_id, form_id):
    with create_session() as session:
        form = session.query(Form).filter(Form.id == form_id, Form.hidden.is_(False)).first()
        if form is None:
            raise KeyError(f"Form {form_id} not found")
        association = session.query(FormToEventAssociation) \
            .filter(FormToEventAssociation.form_id == form_id,
                    FormToEventAssociation.event_id == event_id,
                    FormToEventAssociation.hidden.is_(False)).first()

        if association is None:
            raise KeyError(f"Form {form_id} is not added to event {event_id}")
        association.hidden = True


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


def check_day_format(day: str):
    return day.startswith("C") and \
           ((len(day) > 1 and day[1:].isdigit() and int(day[1:]) > 0) or
            (len(day) > 2 and day[1] in "+-" and day[2:].isdigit() and int(day[2:]) > 0))
