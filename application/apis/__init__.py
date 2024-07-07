from flask_restx import Api

from .auth import api as ns1
from .profile import api as ns2


api: Api = Api(prefix="/api/")

api.add_namespace(ns1)
api.add_namespace(ns2)
