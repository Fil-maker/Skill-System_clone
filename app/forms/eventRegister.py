from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, HiddenField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired


class EventRegisterForm(FlaskForm):
    label = "Title"
    title = StringField(label,
                        validators=[DataRequired()],
                        render_kw={
                            "class": "form-control",
                            "required": True,
                            "type": "name",
                            "placeholder": label
                        })

    label = "Start Date"
    start_date = DateTimeLocalField(label,
                                    format='%Y-%m-%dT%H:%M',
                                    validators=[DataRequired()],
                                    render_kw={
                                        "class": "form-control",
                                        "required": True,
                                        "placeholder": label
                                    })

    label = "C1 Date"
    c_date = DateTimeLocalField(label,
                                format='%Y-%m-%dT%H:%M',
                                validators=[DataRequired()],
                                render_kw={
                                    "class": "form-control",
                                    "required": True,
                                    "placeholder": label
                                })

    label = "C+1 Date"
    c1_date = DateTimeLocalField(label,
                                 format='%Y-%m-%dT%H:%M',
                                 validators=[DataRequired()],
                                 render_kw={
                                     "class": "form-control",
                                     "required": True,
                                     "placeholder": label
                                 })
    label = "Finish Date"
    finish_date = DateTimeLocalField(label,
                                     format='%Y-%m-%dT%H:%M',
                                     validators=[DataRequired()],
                                     render_kw={
                                         "class": "form-control",
                                         "required": True,
                                         "placeholder": label
                                     })

    photo = FileField("Attach an image", render_kw={
        "class": "form-control-file btn btn-primary",
        "id": "photoField"
    })

    photo_base64 = HiddenField()

    submit = SubmitField("OK", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def __init__(self, *args, **kwargs):
        super(EventRegisterForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.title.render_kw["class"] = default
        self.start_date.render_kw["class"] = default
        self.c_date.render_kw["class"] = default
        self.c1_date.render_kw["class"] = default
        self.finish_date.render_kw["class"] = default
        self.photo.render_kw["class"] = "form-control-file"
