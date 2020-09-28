from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class PasswordForm(FlaskForm):
    label = "Current password"
    cur_password = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "form-control label",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    label = "New password"
    new_password = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    label = "Repeat password"
    password_again = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    submit = SubmitField("Confirm", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.cur_password.render_kw["class"] = default
        self.new_password.render_kw["class"] = default
        self.password_again.render_kw["class"] = default
