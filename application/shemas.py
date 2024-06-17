from marshmallow import fields, Schema, validate
from marshmallow.fields import Field


data: dict[str, str] = {
    "email": "timir  @m2q.qq33",
    "username": "Lary  00000",          # just for tests
    "password": " 123 41  ",
}

class RegisterSchema(Schema):
    username: Field = fields.Str(validate=validate.Length(6, 20), required=True)
    password: Field = fields.Str(validate=validate.Length(6, 20),  required=True)
    email: Field = fields.Email(required=True)


class LoginSchema(Schema):
    username: Field = fields.Str(validate=validate.Length(6, 20), required=True)
    password: Field = fields.Str(validate=validate.Length(6, 20), required=True)
