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
    amount: Field = fields.Float(
        validate=validate.Range(min=0, min_inclusive=False, max=4_294_967_296)
    )
    type: Field = fields.Str(validate=validate.OneOf(choices=["buy", "sell"]))


class CryptoTransactionSchema(TransactionSchema):
    ticker: Field = fields.Str(required=True, validate=validate.Length(2, 8))


class FiatTransactionSchema(TransactionSchema):
    iso: Field = fields.Str(required=True, validate=validate.Length(2, 8))
