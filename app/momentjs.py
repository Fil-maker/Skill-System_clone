import datetime
from time import strftime

from jinja2 import Markup


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (
            self.timestamp.strftime("%Y-%m-%d"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
