from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class FormSignForm(FlaskForm):
    label = "Enter PIN"
    pin = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "password",
        "maxlength": 4,
        "placeholder": label
    })

    submit = SubmitField("Sign", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def __init__(self, *args, **kwargs):
        super(FormSignForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.pin.render_kw["class"] = default
