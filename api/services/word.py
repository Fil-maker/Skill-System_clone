from io import BytesIO
import os

import requests
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from api.data.db_session import create_session
from api.data.models.form import Form
from api.data.models.user_to_event_association import EventRoles
from api.services.events import get_c_format_from_dates
from api.services.forms import get_form_signatory


def render_form_template(form_id):
    with create_session() as session:
        form = session.query(Form).get(form_id)

        doc = DocxTemplate(os.path.join(os.path.dirname(__file__), "..", "templates", "word", "form.docx"))

        day = get_c_format_from_dates(form.event.start_date, form.event.main_stage_date,
                                      form.event.final_stage_date, form.event.finish_date)[form.date]
        chief_expert = form.event.chief_expert

        r = requests.get(f"{os.environ.get('S3_BUCKET_URL')}/events/init/{form.event.photo_url}")
        bytes_io = BytesIO()
        bytes_io.write(r.content)
        bytes_io.seek(0)

        doc.render({
            "form_title": form.title,
            "day": day,
            "date": form.date,
            "event_title": form.event.title,
            "chief_expert_first_name": chief_expert.first_name if chief_expert else "-",
            "chief_expert_last_name": chief_expert.last_name if chief_expert else "",
            "content": form.content,
            "signatory": [{"role": str(EventRoles(user["role"])), "user": user["user"]} for user in
                          get_form_signatory(form.id)] * 51,
            "image": InlineImage(doc, bytes_io, height=Mm(25))
        })
        doc.save("C:/Users/sssemion/PycharmProjects/skill-management-system/api/services/doc.docx")
