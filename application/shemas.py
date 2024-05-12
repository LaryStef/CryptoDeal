# from flask_marshmallow import Schema
from marshmallow import fields, Schema, validate


datadict = {
    "email": "timir@m2q.qq33",
    "username": "Lary00000",
    "password": "12341",
    "request_id": "1715541060161190",
    "page": "http://127.0.0.1:5000/"
}


class RegisterSchema(Schema):
    username = fields.Str(validate=validate.Length(8, 16), required=True)
    password = fields.Str(validate=validate.Length(8, 16),  required=True)
    email = fields.Email(required=True)
    page = fields.URL()
    request_id = fields.Str(validate=validate.And(
        validate.Length(equal=16),
        validate.Regexp("^[0-9]+$")
    ),  required=True)

