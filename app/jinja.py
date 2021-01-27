import datetime
import os

from jinja2 import Markup


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")

    def render(self, format):
        return Markup(f"<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (
            self.timestamp.strftime("%Y-%m-%d"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def locale(self, fmt):
        return Markup(f"<script>\nmoment.locale('{fmt}');\n</script>")

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


def get_env(key, default):
    return os.environ.get(key, default)