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


class TransactionSchema(Schema):
    amount: Field = fields.Integer(
        validate=validate.Range(min=0, max=4_294_967_296)
    )
    type_: Field = fields.Str(validate=validate.OneOf(choices=["buy", "sell"]))


class CryptoTransactionSchema(TransactionSchema):
    ticker: Field = fields.Str(required=True, validate=validate.Length(3, 8))


class FiatTransactionSchema(TransactionSchema):
    iso: Field = fields.Str(required=True, validate=validate.Length(3, 8))
