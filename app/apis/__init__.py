from flask_restx import Api

from .auth import api as ns1
from .profile import api as ns2
from .sessions import api as ns3
from .crypto import api as ns4

api: Api = Api(prefix="/api/")

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
api.add_namespace(ns4)
