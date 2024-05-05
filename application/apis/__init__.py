from flask_restx import Api

from .auth import api as ns1


api = Api(prefix="/api/")

api.add_namespace(ns1)
