from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_serializer.lib.timezones import format_dt


class ISO8601SerializerMixin(SerializerMixin):

    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"
    time_format = "%H:%M:%S"

    def serialize_datetime(self, value):
        return format_dt(
            tpl=self.datetime_format,
            dt=value
        )

    def serialize_date(self, value):
        return format_dt(
            tpl=self.date_format,
            dt=value
        )

    def serialize_time(self, value):
        return format_dt(
            tpl=self.time_format,
            dt=value
        )
