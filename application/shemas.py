# from flask_marshmallow import Schema
from marshmallow import fields, Schema, validate


data = {
    "email": "timir  @m2q.qq33",
    "username": "Lary  00000",
    "password": " 123 41  ",
}

class RegisterSchema(Schema):
    username = fields.Str(validate=validate.Length(6, 20), required=True)
    password = fields.Str(validate=validate.Length(6, 20),  required=True)
    email = fields.Email(required=True)
