import datetime
from io import BytesIO
import os

import requests
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from api.data.db_session import create_session
from api.data.models import FormToEventAssociation
from api.data.models.user_to_event_association import EventRoles
from api.services.events import get_dates_from_c_format
from api.services.forms import get_form_signatory


def render_form_template(event_id, form_id) -> BytesIO:
    with create_session() as session:
        association = session.query(FormToEventAssociation) \
            .filter(FormToEventAssociation.form_id == form_id,
                    FormToEventAssociation.event_id == event_id).first()
        event = association.event
        form = association.form

        doc = DocxTemplate(
            os.path.join(os.path.dirname(__file__), "..", "templates", "word", "form.docx"))

        date = get_dates_from_c_format(event.start_date, event.main_stage_date,
                                       event.final_stage_date, event.finish_date)[form.day]
        chief_expert = event.chief_expert

        params = {
            "form_title": form.title,
            "day": form.day,
            "date": date,
            "event_title": event.title,
            "chief_expert_first_name": chief_expert.first_name if chief_expert else "-",
            "chief_expert_last_name": chief_expert.last_name if chief_expert else "",
            "content": form.content,
            "signatory": [{"role": str(EventRoles(item["participant"]["role"])),
                           "user": item["participant"]["user"]}
                          for item in get_form_signatory(event_id, form_id)],
            "now": str(datetime.datetime.now())
        }

        bytes_io = BytesIO()
        if event.photo_url is not None:
            r = requests.get(f"{os.environ.get('S3_BUCKET_URL')}/events/init/{event.photo_url}")
            bytes_io.write(r.content)
            bytes_io.seek(0)
            params["image"] = InlineImage(doc, bytes_io, height=Mm(30))

        doc.render(params)
        bytes_io.close()

        file = BytesIO()
        doc.save(file)
        file.seek(0)
        return file
