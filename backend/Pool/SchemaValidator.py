
from datetime import datetime
from marshmallow import Schema, fields, validate


def validate_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError as e:
        return False
    return True

class ReservationItemSchema(Schema):
    date = fields.Str(required=True, validate=validate_date)
    time = fields.Str(required=True, \
            load_from='time', \
            attribute='time', \
            data_key='time', \
            validate=validate.OneOf(["8-10", "10-12", "12-14", "14-16", "16-18", "18-20"]))
    lane = fields.Number(required=False, \
            validate=lambda x: x >= 1 and x <= 8)

class ReservationSchema(Schema):
    time = fields.Str(required=True, \
            load_from='time', \
            attribute='time', \
            data_key='time', \
            validate=validate.OneOf(["8-10", "08-10", "10-12", "12-14", "14-16", "16-18", "18-20"]))
    others = fields.List(fields.Nested(ReservationItemSchema), required=False)

class ReservationDetailSchema(Schema):
    reservations = fields.List(fields.Nested(ReservationItemSchema), required=True)


