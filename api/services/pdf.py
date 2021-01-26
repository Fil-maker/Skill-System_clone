import datetime
import os
from html import unescape
from io import BytesIO

import markdown
from fpdf import FPDF, HTMLMixin
from fpdf.html import HTML2FPDF

from api.data.db_session import create_session
from api.data.models import FormToEventAssociation
from api.data.models.user_to_event_association import EventRoles
from api.services.events import get_dates_from_c_format
from api.services.forms import get_form_signatory


def render_pdf(event_id, form_id) -> BytesIO:
    with create_session() as session:
        association = session.query(FormToEventAssociation) \
            .filter(FormToEventAssociation.form_id == form_id,
                    FormToEventAssociation.event_id == event_id).first()
        event = association.event
        form = association.form
        date = get_dates_from_c_format(event.start_date, event.main_stage_date,
                                       event.final_stage_date, event.finish_date)[form.day]
        chief_expert = event.chief_expert

        signatory = [{"role": str(EventRoles(item["participant"]["role"])),
                      "user": item["participant"]["user"]}
                     for item in get_form_signatory(event_id, form_id)]

        pdf = FormPDF(form.title, form.day, date, event.title,
                      chief_expert.first_name if chief_expert else "-",
                      chief_expert.last_name if chief_expert else "",
                      form.content, signatory,
                      f"{os.environ.get('S3_BUCKET_URL')}/events/init/{event.photo_url}" if event.photo_url else None)

        file = BytesIO()
        file.write(pdf.output(dest="S"))
        file.seek(0)
        return file


class FixedHTMLMixin(HTMLMixin):
    def write_html(self, h, text, *args, **kwargs):
        h2p = HTML2FPDF(self, *args, **kwargs)
        h2p.h = h
        text = unescape(text)
        h2p.feed(text)


class FormPDF(FPDF, FixedHTMLMixin):
    def __init__(self, form_title, day, date, event_title, chief_expert_first_name,
                 chief_expert_last_name, content, signatory, image_url=None):
        super(FormPDF, self).__init__(unit="pt")
        # Page size: a4 (595.28 x 841.89 pt)

        self.form_title = form_title
        self.day = day
        self.date = date
        self.event_title = event_title
        self.chief_expert_first_name = chief_expert_first_name
        self.chief_expert_last_name = chief_expert_last_name
        self.content = content
        self.signatory = signatory
        self.image_url = image_url

        self.add_font("MarckScript", fname="api/static/fonts/MarckScript/MarckScript-Regular.ttf", uni=True)
        self.add_font("akrobat", "", fname="api/static/fonts/Akrobat/Akrobat-Regular.ttf", uni=True)
        self.add_font("akrobat", "B", fname="api/static/fonts/Akrobat/Akrobat-Bold.ttf", uni=True)

        self.set_auto_page_break(1, 25)
        self.fill_document()

    def fill_document(self):
        self.add_page()
        self.add_image()
        self.add_main_body()
        self.add_signatory_table()

    def add_image(self):
        if self.image_url is not None:
            self.image(self.image_url, 470.28, 25, 100, 100)
            self.set_y(125)

    def add_main_body(self):
        self.set_font("akrobat", "B", 18)
        self.cell(0, 20, self.form_title, 0, 1, "C")

        self.set_y(self.get_y() + 5)
        self.set_font("akrobat", "", 12)
        for k, v in (
                ("Day:", f"{self.day} ({self.date})"),
                ("Event:", self.event_title),
                ("Skill", "Skill Name"),
                ("Chief Expert:", self.chief_expert_first_name + " " + self.chief_expert_last_name)
        ):
            self.set_x(25)
            self.cell(150, 15, k, 0, 0)
            self.cell(0, 15, v, 0, 1)

        self.set_xy(self.l_margin, self.get_y() + 20)
        html = "<font color='#000000' size='12' face='akrobat'" + markdown.markdown(self.content) + "</font>"
        html = html.replace("<strong>", "<b>").replace("</strong>", "</b>")
        self.write_html(15, html)

    def add_signatory_table(self):
        self.set_y(self.get_y() + 25)

        self.add_heading_for_signatory_table(len(self.signatory) <= 1)
        if not self.signatory:
            self.set_font("akrobat", "", 12)
            self.set_text_color(128, 128, 128)
            self.set_x(50)
            self.cell(222.64, 20, "No signatures yet", 1, 1, "C")

        for i in range(len(self.signatory)):
            role = self.signatory[i]["role"]
            user = self.signatory[i]["user"]

            if i % 2 == 0:
                x = 50
            else:
                x = 322.64

            if self.get_y() + 20 >= self.page_break_trigger:
                self.add_heading_for_signatory_table(i == len(self.signatory) - 1)

            self.set_x(x)
            self.set_font("MarckScript", "", 14)
            self.set_text_color(65, 105, 225)
            self.cell(222.64, 10, user["last_name"], "LTR", 1, "R")

            self.set_x(x)
            self.set_font("akrobat", "", 8)
            self.set_text_color(0, 0, 0)
            self.cell(222.64, 10, f"{role} {user['first_name']} {user['last_name']}", "LBR", 1, "L")

            if i % 2 == 0:
                self.set_y(self.get_y() - 20)

    def add_heading_for_signatory_table(self, only_left=False):
        self.set_x(50)
        self.set_font("akrobat", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(222.64, 20, "Sign", 1, int(only_left), "C")

        if not only_left:
            self.set_x(322.64)
            self.cell(222.64, 20, "Sign", 1, 1, "C")

    def footer(self):
        self.rect(15, 15, 565.28, 811.89)

        self.set_font("akrobat", size=8)
        self.set_text_color(128, 128, 128)
        self.set_xy(15, -15)
        self.cell(282.64, 15, f"Page {self.page_no()}", align="L")
        self.cell(282.64, 15, datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), align="R")
