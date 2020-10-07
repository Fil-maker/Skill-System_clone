from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class EditEventInformationForm(FlaskForm):
    label = "Event Title"
    title = StringField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "name",
        "placeholder": label
    })

    submit = SubmitField("Change", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def __init__(self, *args, **kwargs):
        super(EditEventInformationForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.title.render_kw["class"] = default
