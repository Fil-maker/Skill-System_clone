from flask import g
from flask_restful import abort

from api.data.db_session import create_session
from api.data.models import Event, UserToEventAssociation
from api.data.models.form import Form
from api.data.models.user_to_event_association import EventRoles
from api.services.events import get_dates_from_c_format


def abort_if_form_not_found(func):
    def new_func(self, form_id):
        with create_session() as session:
            event = session.query(Form).get(form_id)
            if not event:
                abort(404, success=False, message=f"Form {form_id} not found")
            return func(self, form_id)

    return new_func


def get_form(form_id=None, event_id=None):
    with create_session() as session:
        if form_id is not None:
            return session.query(Form).get(form_id).to_dict()
        elif event_id is not None:
            return [item.to_dict() for item in session.query(Event).get(event_id).forms]


def delete_form(form_id):
    with create_session() as session:
        user = session.query(Form).get(form_id)
        session.delete(user)


def create_form(title, content, day, role, event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        if Event is None:
            raise KeyError(f"Event {event_id} not found")
        form = Form(title=title,
                    content=content,
                    role=role)
        if not (len(day) > 1 and day[0] == "C" and
                (day[1:].isdigit() or (len(day) > 2 and day[1] in "-+" and day[2:].isdigit()))):
            raise ValueError(f"Day {day} format is incorrect")
        date = get_dates_from_c_format(event.start_date, event.main_stage_date,
                                       event.final_stage_date, event.finish_date).get(day, None)
        if date is not None:
            form.date = date
        else:
            raise KeyError(f"Event doesn't have day {day}")
        event.forms.append(form)
        session.commit()
        return form.to_dict()


def update_form(form_id, title=None, content=None, day=None):
    with create_session() as session:
        form = session.query(Form).get(form_id)
        if title:
            form.title = title
        if content:
            form.content = content
        if day:
            if not (len(day) > 1 and day[0] == "C" and
                    (day[1:].isdigit() or (len(day) > 2 and day[1] in "-+" and day[2:].isdigit()))):
                raise ValueError(f"Day {day} format is incorrect")
            event = form.event
            date = get_dates_from_c_format(event.start_date, event.main_stage_date,
                                           event.final_stage_date, event.finish_date).get(day, None)
            if date is not None:
               form.date = date
            else:
                raise KeyError(f"Event doesn't have day {day}")
        return form.to_dict()


def get_form_signatory(form_id):
    with create_session() as session:
        form = session.query(Form).get(form_id)
        return [user.to_dict() for user in form.signatory]


def sign_form(form_id, pin):
    with create_session() as session:
        form = session.query(Form).get(form_id)
        cur_user = session.query(UserToEventAssociation).filter(
            UserToEventAssociation.user_id == g.current_user.id,
            UserToEventAssociation.event_id == form.event_id).first()
        if cur_user in form.event.participants and (
                cur_user.role == form.role or
                EventRoles(cur_user.role) == EventRoles.CHIEF_EXPERT):
            if g.current_user.pin is None:
                raise ValueError("Pin is not set")
            elif not g.current_user.check_pin(str(pin)):
                raise ValueError("Incorrect pin")
            else:
                form.signatory.append(cur_user.participant)
                return True
        else:
            raise KeyError
