from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField, FileField
from wtforms.validators import DataRequired


class EditEventInformationForm(FlaskForm):
    label = "Event Title"
    title = StringField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "name",
        "placeholder": label
    })

    photo = FileField("Attach an image", render_kw={
        "class": "form-control-file btn btn-primary",
        "id": "photoField"
    })

    photo_base64 = HiddenField()

    submit = SubmitField("Change",
                         render_kw={
                             "class": "btn btn-primary",
                         })

    def __init__(self, *args, **kwargs):
        super(EditEventInformationForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.title.render_kw["class"] = default
        self.photo.render_kw["class"] = "form-control-file"
