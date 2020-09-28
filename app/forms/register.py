from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired

from app.services.users import get_countries_list, get_regions_list, get_ru_id


class RegisterForm(FlaskForm):
    label = "Name"
    first_name = StringField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "name",
        "placeholder": label
    })

    label = "Surname"
    last_name = StringField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "surname",
        "placeholder": label
    })

    label = "Country"
    country = SelectField(label,
                          choices=[(item["id"], item["name"]) for item in get_countries_list()],
                          validators=[DataRequired()],
                          render_kw={
                              "class": "form-control",
                              "required": True,
                              "id": "cntry-fld",
                              "placeholder": label,
                              "data-ru_id": get_ru_id()
                          })

    label = "Region"
    region = SelectField(label,
                         choices=[(item["id"], item["name"]) for item in get_regions_list()],
                         validators=[DataRequired()],
                         render_kw={
                             "class": "form-control",
                             "required": True,
                             "placeholder": label
                         })

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

    label = "Repeat password"
    password_again = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    photo = FileField("Attach an image", render_kw={
        "class": "form-control-file",
        "id": "photoField"
    })
    submit = SubmitField("OK", render_kw={
        "class": "button btn btn-primary",
        "type": "submit"
    })
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.email.render_kw["class"] = default
        self.first_name.render_kw["class"] = default
        self.last_name.render_kw["class"] = default
        self.country.render_kw["class"] = default
        self.region.render_kw["class"] = default
        self.photo.render_kw["class"] = default
        self.password.render_kw["class"] = default
        self.password_again.render_kw["class"] = default