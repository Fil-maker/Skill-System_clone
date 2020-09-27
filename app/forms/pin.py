from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class PinForm(FlaskForm):
    label = "Enter PIN"
    password = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    submit = SubmitField("Change", render_kw={
        "class": "button btn btn-primary",
        "type": "submit"
    })
