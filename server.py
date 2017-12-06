from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse, abort
from flask_sslify import SSLify

import sys
import os
import postgresql
import postgresql.exceptions
import configparser
from pathlib import Path

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
self.config = configparser.ConfigParser()
self.config._interpolation = configparser.ExtendedInterpolation()

if not Path('secret.yml').exists():
    print("Looking for secrets in environment")
    env = os.environ['secret']
    if env is not None:
        self.config.read(env)
    else:
        raise FileNotFoundError('No config available.')
else:
    self.config.read('secret.yml')

self.secret = self.config['DEFAULT']
self.db = postgresql.open(self.secret.get('pg_uri'))

# MODELS
user = self._api.model('User', {
    'pseudo': fields.String,
    'trigram': fields.String,
})

# PARSERS
parser_create_user = reqparse.RequestParser()
parser_create_user.add_argument('pseudo', type=str, required=True)
parser_create_user.add_argument('trigram', type=str, required=True)

# SQL COMMANDS
create_user = self.db.prepare("INSERT INTO users (trigram, pseudo) VALUES ($1, $2)")
get_users = self.db.prepare("SELECT id, trigram, pseudo FROM users")
get_user_by_id = self.db.prepare("SELECT id, trigram, pseudo FROM users WHERE id = $1 LIMIT 1")
delete_user = self.db.prepare("DELETE FROM users WHERE id = $1")


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


@self.v1.route("/users")
class Users(Resource):
    def post(self):
        args = parser_create_user.parse_args()
        try:
            create_user(args['trigram'], args['pseudo'])
        except postgresql.exceptions.UniqueError:
            abort(400, "Duplicated user")
        return "User created"

    def get(self):
        users = get_users()
        res = []
        if user is None:
            abort(404)
        for u in users:
            res.append({
                'id': u[0],
                'pseudo': u[2],
                'trigram': u[1],
            })
        return res


@self.v1.route("/users/<int:user_id>")
class User(Resource):
    def get(self, user_id):
        user = get_user_by_id.first(user_id)
        if user is None:
            abort(404)
        return {
            'id': user[0],
            'pseudo': user[2],
            'trigam': user[1],
        }

    def delete(self, user_id):
        delete_user(user_id)
        return "User deleted"





