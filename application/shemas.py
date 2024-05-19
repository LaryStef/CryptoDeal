# from flask_marshmallow import Schema
from marshmallow import fields, Schema, validate


datadict = {
    "email": "timir@m2q.qq33",
    "username": "Lary00000",
    "password": "12341",
}


class RegisterSchema(Schema):
    username = fields.Str(validate=validate.Length(6, 20), required=True)
    password = fields.Str(validate=validate.Length(6, 20),  required=True)
    email = fields.Email(required=True)
