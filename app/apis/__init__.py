from flask_restx import Api

from app.apis.auth import api as ns1
from app.apis.crypto import api as ns4
from app.apis.user import api as ns2
from app.apis.sessions import api as ns3


api: Api = Api(prefix="/api/")

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
api.add_namespace(ns4)
