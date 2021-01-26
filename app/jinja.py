import datetime
import markdown
from jinja2 import Markup


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")

    def render(self, format):
        return Markup(f"<script>document.write(moment(\"%s\").%s);</script>" % (
            self.timestamp.strftime("%Y-%m-%d"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def locale(self, fmt):
        return Markup(f"<script>moment.locale('{fmt}');</script>")

    def calendar(self):
        return self.render("calendar()")

    def from_now(self):
        return self.render("fromNow()")

    def is_able_to_sign(self):
        return datetime.datetime.now() >= self.timestamp


class text(object):

    def __init__(self, string):
        self.string = string

    def short(self, length=10):
        return ' '.join(self.string.split()[:length]) + ' ...'

    def markdown(self):
        md = markdown.markdown(self.string).replace('\n', '<div></div>')
        return Markup(f"""<script>document.write('{md}');</script>""")
