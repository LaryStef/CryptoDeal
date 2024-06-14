from marshmallow import fields, Schema, validate


data = {
    "email": "timir  @m2q.qq33",
    "username": "Lary  00000",          # just for tests
    "password": " 123 41  ",
}

class RegisterSchema(Schema):
    username = fields.Str(validate=validate.Length(6, 20), required=True)
    password = fields.Str(validate=validate.Length(6, 20),  required=True)
    email = fields.Email(required=True)


class LoginSchema(Schema):
    username = fields.Str(validate=validate.Length(6, 20), required=True)
    password = fields.Str(validate=validate.Length(6, 20), required=True)
