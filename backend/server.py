from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sslify import SSLify

import sys

self = sys.modules[__name__]

# ATTRIBUTES
_app = None
_sslify = None
_api = None


# INIT
self._app = Flask(__name__)
self._sslify = SSLify(self._app)
self._api = Api(self._app,
                version="alpha",
                title="EkiTag API",
                description="Custom tagpro matchmaking and ranking API")


# GETTERS
def app():
    """Return the app object.

    Returns:
        the app object.

    """
    return self._app


def api():
    """Return the api object.

    Returns:
        the api object.

    """
    return self._api


# NAMESPACE V1
self.v1 = self._api.namespace(name="v1", validate=True)


@self.v1.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return "Hello World !"
