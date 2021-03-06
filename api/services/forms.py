import datetime

from flask import g
from flask_restful import abort

from api.data.db_session import create_session
from api.data.models import UserToEventAssociation, FormToEventAssociation, Event, FormMustSignAssociation
from api.data.models.form import Form
from api.data.models.form_signatory_association import FormSignatoryAssociation
from api.data.models.user_to_event_association import EventRoles
from api.services.events import check_day_format, get_dates_from_c_format


def abort_if_form_not_found(func):
    def new_func(self, form_id):
        with create_session() as session:
            form = session.query(Form).filter(Form.id == form_id, Form.hidden.is_(False)).first()
            if not form:
                abort(404, success=False, message=f"Form {form_id} not found")
            return func(self, form_id)

    return new_func


def abort_if_event_form_not_found(func):
    def new_func(self, event_id, form_id):
        with create_session() as session:
            event = session.query(Event).filter(Event.id == event_id, Event.hidden.is_(False)).first()
            form = session.query(Form).filter(Form.id == form_id, Form.hidden.is_(False)).first()
            if not event:
                abort(404, success=False, message=f"Event {event_id} not found")
            if not form:
                abort(404, success=False, message=f"Form {form_id} not found")
            association = session.query(FormToEventAssociation) \
                .filter(FormToEventAssociation.form_id == form_id,
                        FormToEventAssociation.event_id == event_id,
                        FormToEventAssociation.hidden.is_(False)).first()
            if association is None:
                abort(404, success=False, message=f"Form {form_id} is not added to event")
            return func(self, event_id, form_id)

    return new_func


def get_form(form_id=None):
    with create_session() as session:
        if form_id is not None:
            return session.query(Form).get(form_id).to_dict()
        return [item.to_dict() for item in session.query(Form).filter(Form.hidden.is_(False)).all()]


def delete_form(form_id):
    with create_session() as session:
        form = session.query(Form).get(form_id)
        if form.events.filter(FormToEventAssociation.hidden.is_(False)).count() > 0:
            raise ValueError("Form that is used cannot be deleted")
        form.hidden = True


def create_form(title, content, day, role):
    if not check_day_format(day):
        raise ValueError("Incorrect day format")
    with create_session() as session:
        form = Form(title=title,
                    content=content,
                    role=role,
                    day=day)
        session.add(form)
        session.commit()
        return form.to_dict()


def update_form(form_id, title=None, content=None, day=None, role=None):
    if not check_day_format(day):
        raise ValueError("Incorrect day format")
    with create_session() as session:
        form = session.query(Form).get(form_id)
        if form.events.filter(FormToEventAssociation.hidden.is_(False)).count() > 0:
            raise ValueError("Form that is used cannot be changed")
        if title:
            form.title = title
        if content:
            form.content = content
        if day:
            form.day = day
        if role:
            form.role = role
        return form.to_dict()


def get_event_form(event_id, form_id):
    with create_session() as session:
        form_to_event = session.query(FormToEventAssociation) \
            .filter(FormToEventAssociation.event_id == event_id,
                    FormToEventAssociation.form_id == form_id,
                    FormToEventAssociation.hidden.is_(False)).first()
        return form_to_event.to_dict()


def get_form_signatory(event_id, form_id):
    with create_session() as session:
        data = session.query(UserToEventAssociation, FormToEventAssociation, FormSignatoryAssociation) \
            .join(FormToEventAssociation, FormToEventAssociation.event_id == UserToEventAssociation.event_id) \
            .join(FormSignatoryAssociation, FormSignatoryAssociation.form_to_event_id == FormToEventAssociation.id) \
            .filter(FormToEventAssociation.event_id == event_id,
                    FormToEventAssociation.form_id == form_id,
                    FormToEventAssociation.hidden.is_(False),
                    UserToEventAssociation.event_id == FormToEventAssociation.event_id,
                    FormToEventAssociation.id == FormSignatoryAssociation.form_to_event_id,
                    UserToEventAssociation.user_id == FormSignatoryAssociation.user_id
                    )
        resp = []
        for user_to_event, form_to_event, signatory in data:
            resp.append({
                "participant": user_to_event.to_dict_participant(),
                **signatory.to_dict(only=["sign_date"])
            })
        return resp


def sign_form(event_id, form_id, pin):
    with create_session() as session:
        association = session.query(FormToEventAssociation) \
            .filter(FormToEventAssociation.form_id == form_id,
                    FormToEventAssociation.event_id == event_id,
                    FormToEventAssociation.hidden.is_(False)).first()
        cur_user = session.query(UserToEventAssociation) \
            .filter(UserToEventAssociation.user_id == g.current_user.id,
                    UserToEventAssociation.event_id == event_id).first()
        if cur_user in association.event.participants and (
                cur_user.role == association.form.role or
                EventRoles(cur_user.role) == EventRoles.CHIEF_EXPERT):
            if association.date > datetime.date.today():
                raise ValueError(f"You can't sign the form before {association.date}")
            if g.current_user.pin is None:
                raise ValueError("Pin is not set")
            elif not g.current_user.check_pin(str(pin)):
                raise ValueError("Incorrect pin")
            else:
                must_sign = session.query(FormMustSignAssociation).filter(
                    FormMustSignAssociation.form_to_event_id == association.id,
                    FormMustSignAssociation.user_id == g.current_user.id
                ).first()
                session.delete(must_sign)
                signatory = FormSignatoryAssociation(form_to_event_id=association.id,
                                                     user_id=g.current_user.id)
                session.add(signatory)
                return True
        else:
            raise KeyError
