from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

from api.services.users import get_countries_list, get_regions_list, get_ru_id


class EditProfileForm(FlaskForm):
    label = "Name"
    first_name = StringField(label,
                             validators=[DataRequired()],
                             render_kw={
                                 "class": "input-str form-control",
                                 "required": True,
                                 "placeholder": label
                             })

    label = "Surname"
    last_name = StringField(label,
                            validators=[DataRequired()],
                            render_kw={
                                "class": "input-str form-control",
                                "required": True,
                                "placeholder": label
                            })

    label = "Country"
    country = SelectField(label,
                          choices=[(item["id"], item["name"]) for item in get_countries_list()],
                          validators=[DataRequired()],
                          render_kw={
                              "class": "input-str form-control",
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
                             "class": "input-str form-control",
                             "required": True,
                             "id": "region-fld",
                             "placeholder": label
                         })

    label = "About"
    about = TextAreaField(label,
                          render_kw={
                              "class": "input-str form-control",
                              "type": "text",
                              "placeholder": label
                          })

    photo = FileField("Attach an image", render_kw={
        "class": "form-control-file btn btn-primary",
        "id": "photoField"
    })

    photo_base64 = HiddenField()

    submit = SubmitField("OK",
                         render_kw={
                             "class": "btn btn-primary"
                         })

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.first_name.render_kw["class"] = default
        self.last_name.render_kw["class"] = default
        self.country.render_kw["class"] = default
        self.region.render_kw["class"] = default
        self.about.render_kw["class"] = default
        self.photo.render_kw["class"] = "form-control-file"
