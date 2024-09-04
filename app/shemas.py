from marshmallow import Schema, fields, validate
from marshmallow.fields import Field


class RegisterSchema(Schema):
    username: Field = fields.Str(
        validate=validate.Length(6, 20),
        required=True
    )
    password: Field = fields.Str(
        validate=validate.Length(6, 20),
        required=True
    )
    email: Field = fields.Email(required=True)


class LoginSchema(Schema):
    username: Field = fields.Str(
        validate=validate.Length(6, 20),
        required=True
    )
    password: Field = fields.Str(
        validate=validate.Length(6, 20),
        required=True
    )
    device: Field = fields.Str(validate=validate.Length(6, 30))
