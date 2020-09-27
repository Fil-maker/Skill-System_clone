from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class PasswordForm(FlaskForm):
    label = "Current password"
    curPassword = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control label",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    label = "New password"
    newPassword = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    label = "Repeat password"
    passwordAgain = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    submit = SubmitField("Confirm", render_kw={
        "class": "button btn btn-primary",
        "type": "submit"
    })
