from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class EditEventDatesForm(FlaskForm):
    label = "Start Date"
    start_date = DateField(label,
                           format='%Y-%m-%d',
                           validators=[DataRequired()],
                           render_kw={
                               "class": "form-control",
                               "required": True,
                               "placeholder": label
                           })

    label = "C1 Date"
    main_stage_date = DateField(label,
                                format='%Y-%m-%d',
                                validators=[DataRequired()],
                                render_kw={
                                    "class": "form-control",
                                    "required": True,
                                    "placeholder": label
                                })

    label = "C+1 Date"
    final_stage_date = DateField(label,
                                 format='%Y-%m-%d',
                                 validators=[DataRequired()],
                                 render_kw={
                                     "class": "form-control",
                                     "required": True,
                                     "placeholder": label
                                 })
    label = "Finish Date"
    finish_date = DateField(label,
                            format='%Y-%m-%d',
                            validators=[DataRequired()],
                            render_kw={
                                "class": "form-control",
                                "required": True,
                                "placeholder": label
                            })

    submit = SubmitField("OK", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def __init__(self, *args, **kwargs):
        super(EditEventDatesForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.start_date.render_kw["class"] = default
        self.main_stage_date.render_kw["class"] = default
        self.final_stage_date.render_kw["class"] = default
        self.finish_date.render_kw["class"] = default
