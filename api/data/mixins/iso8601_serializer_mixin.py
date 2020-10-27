from sqlalchemy_serializer import SerializerMixin


class ISO8601SerializerMixin(SerializerMixin):

    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"
    time_format = "%H:%M:%S"
