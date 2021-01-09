from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class FormRegisterForm(FlaskForm):
    label = "From Title"
    title = StringField(label,
                        validators=[DataRequired()],
                        render_kw={
                            "required": True,
                            "placeholder": label
                        })

    label = "Day"
    day = StringField(label,
                      validators=[DataRequired()],
                      render_kw={
                          "required": True,
                          "pattern": "C[-+]?[1-9][0-9]*",
                          "placeholder": label
                      })

    label = "From Content"
    content = TextAreaField(label,
                            validators=[DataRequired()],
                            render_kw={
                                "class": "form-content",
                                "required": True,
                                "placeholder": label
                            })

    label = "For"
    role = RadioField(label,
                      choices=[(0, 'Experts'), (1, 'Competitors')],
                      validators=[DataRequired()],
                      render_kw={
                          "required": True,
                      })

    errors = HiddenField(render_kw={})

    submit = SubmitField("OK",
                         render_kw={
                             "class": "btn btn-primary",
                             "type": "submit"
                         })

    def __init__(self, *args, **kwargs):
        super(FormRegisterForm, self).__init__(*args, **kwargs)
        default = "form-control"
        radio = "input-group-prepend"
        self.title.render_kw["class"] = default
        self.day.render_kw["class"] = default
        self.content.render_kw["class"] = default + " form-content"
        self.role.render_kw["class"] = radio
        self.errors.render_kw["class"] = default
