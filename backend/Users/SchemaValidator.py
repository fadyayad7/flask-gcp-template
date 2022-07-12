
from marshmallow import Schema, fields, validate


class PostUserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(1))
