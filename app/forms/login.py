from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    label = "Email"
    email = StringField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "email",
        "placeholder": label
    })

    label = "Password"
    password = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    submit = SubmitField("Enter", render_kw={
        "class": "button btn btn-primary",
        "type": "submit"
    })

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.email.render_kw["class"] = default
        self.password.render_kw["class"] = default
