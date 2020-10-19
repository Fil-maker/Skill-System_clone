from flask_restful import abort

from api.data.db_session import create_session
from api.data.models import Event
from api.data.models.form import Form


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


def create_form(title, content, date, role, event_id):
    with create_session() as session:
        event = session.query(Event).get(event_id)
        if Event is None:
            raise KeyError(f"Event {event_id} not found")
        # TODO 1
        form = Form(title=title,
                    content=content,
                    date=date,
                    role=role)
        event.forms.append(form)
        session.commit()
        return form.to_dict()


def update_form(form_id, title=None, content=None, date=None):
    with create_session() as session:
        form = session.query(Form).get(form_id)
        if title:
            form.title = title
        if content:
            form.content = content
        if date:
            form.date = date  # TODO 1
        return form.to_dict()
