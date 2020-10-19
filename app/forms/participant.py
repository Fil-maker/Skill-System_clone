from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class ParticipantForm(FlaskForm):
    label = "Email"
    email = StringField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "email",
        "placeholder": label
    })

    submit = SubmitField("Add", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.email.render_kw["class"] = default
