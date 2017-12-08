# -*- coding: utf-8 -*-
from flask import Flask
from flask_restplus import Api, Resource, reqparse, abort
from flask_sslify import SSLify

import postgresql.exceptions
import postgresql.types

from views import createViews
from orm import *
import config

# ========================= INIT

_app = Flask(__name__)
_sslify = SSLify(_app)
api = Api(_app,
          version="alpha",
          title="EkiTag API",
          description="Custom tagpro matchmaking and ranking API")
secret = config.secret()
createViews(api)

# ========================= INPUT PARSERS

parser_create_user = reqparse.RequestParser()
parser_create_user.add_argument('pseudo', type=str, required=True, location='form')
parser_create_user.add_argument('trigram', type=str, required=True, location='form')

parser_update_user = reqparse.RequestParser()
parser_update_user.add_argument('pseudo', type=str, required=True, location='form')
parser_update_user.add_argument('usual_pseudos', type=str, required=True, action='append', location='form')

parser_validate_match = reqparse.RequestParser()
parser_validate_match.add_argument('b1_id', type=int, required=True, location='form')
parser_validate_match.add_argument('b2_id', type=int, location='form')
parser_validate_match.add_argument('b3_id', type=int, location='form')
parser_validate_match.add_argument('b4_id', type=int, location='form')
parser_validate_match.add_argument('b5_id', type=int, location='form')
parser_validate_match.add_argument('b6_id', type=int, location='form')
parser_validate_match.add_argument('r1_id', type=int, required=True, location='form')
parser_validate_match.add_argument('r2_id', type=int, location='form')
parser_validate_match.add_argument('r3_id', type=int, location='form')
parser_validate_match.add_argument('r4_id', type=int, location='form')
parser_validate_match.add_argument('r5_id', type=int, location='form')
parser_validate_match.add_argument('r6_id', type=int, location='form')


# ========================= GETTERS

def app():
    """Return the app object.

    Returns:
        the app object.

    """
    return _app


# ========================= NAMESPACE V1

v1 = api.namespace(name="v1", validate=True)


@v1.route("/users")
class Users(Resource):
    @api.marshal_with(api.models['Message'])
    @api.expect(parser_create_user)
    def post(self):
        args = parser_create_user.parse_args()
        try:
            user_id = create_user.first(args['trigram'], args['pseudo'])
        except postgresql.exceptions.UniqueError:
            abort(400, "Duplicated user")
        return {
            'message': 'User created',
            'value': user_id,
        }

    @api.marshal_with(api.models['UserMin'], as_list=True)
    def get(self):
        users = to_json(get_users())
        if users is None:
            abort(404)
        return users


@v1.route("/users/<int:user_id>")
class User(Resource):
    @api.marshal_with(api.models['User'])
    def get(self, user_id):
        user = to_json(get_user_by_id.first(user_id))
        if user is None:
            abort(404)
        return user

    @api.marshal_with(api.models['Message'])
    @api.expect(parser_update_user)
    def put(self, user_id):
        args = parser_update_user.parse_args()
        update_user(user_id, args['pseudo'], args['usual_pseudos'])
        return {
            'message': 'User updated',
        }

    @api.marshal_with(api.models['Message'])
    def delete(self, user_id):
        desactivate_user(user_id)
        return {
            'message': 'User deleted'
        }


@v1.route("/users/<int:user_id>/matches")
class UserMatches(Resource):
    @api.marshal_with(api.models['MatchMin'], as_list=True)
    def get(self, user_id):
        matches = to_json(get_user_matches(user_id))
        if matches is None:
            abort(404)
        return matches


@v1.route("/matches")
class Matches(Resource):
    @api.marshal_with(api.models['MatchMin'], as_list=True)
    def get(self):
        matches = to_json(get_matches())
        if matches is None:
            abort(404)
        return matches


@v1.route("/matches/<int:match_id>")
class Match(Resource):
    @api.marshal_with(api.models['Match'])
    def get(self, match_id):
        match = to_json(get_match_by_id.first(match_id))
        if match is None:
            abort(404)
        return match

    @api.marshal_with(api.models['Message'])
    def delete(self, match_id):
        delete_match_stats(match_id)
        delete_match(match_id)
        return {
            'message': 'Match deleted',
        }


@v1.route("/matches/<int:match_id>/stats")
class MatchStats(Resource):
    @api.marshal_with(api.models['StatMin'], as_list=True)
    def get(self, match_id):
        match = to_json(get_match_stats(match_id))
        if match is None:
            abort(404)
        return match


@v1.route("/matches/pending")
class MatchesPending(Resource):
    @api.marshal_with(api.models['MatchPending'], as_list=True)
    def get(self):
        matches = to_json(get_pending_matches())
        if matches is None:
            abort(404)
        return matches


@v1.route("/matches/pending/<int:match_id>")
class MatchPending(Resource):
    @api.marshal_with(api.models['MatchPending'])
    def get(self, match_id):
        match = to_json(get_pending_match_by_id.first(match_id))
        if match is None:
            abort(404)
        return match

    @api.expect(parser_validate_match)
    def put(self, match_id):
        def mapper(color):
            for i in range(1, 7):
                pseudo_id_map[pending_match[color + str(i) + "_pseudo"]] = args[color + str(i) + "_id"]
        args = parser_validate_match.parse_args()
        pending_match = to_json(get_pending_match_by_id.first(match_id))
        pending_stats = to_json(get_pending_match_stats(match_id))
        if pending_match is None:
            abort(404)
        pseudo_id_map = {}
        mapper('r')
        mapper('b')
        new_match_id = None
        try:
            with db.xact():
                new_match_id = create_match.first(pending_match['b_score'],
                                                  pending_match['r_score'],
                                                  pending_match['datetime'],
                                                  args['b1_id'],
                                                  args['b2_id'],
                                                  args['b3_id'],
                                                  args['b4_id'],
                                                  args['b5_id'],
                                                  args['b6_id'],
                                                  args['r1_id'],
                                                  args['r2_id'],
                                                  args['r3_id'],
                                                  args['r4_id'],
                                                  args['r5_id'],
                                                  args['r6_id'],
                                                  1)
                for stats in pending_stats:
                    create_stats(new_match_id,
                                 pseudo_id_map[stats['user_pseudo']],
                                 stats['score'],
                                 stats['tags'],
                                 stats['popped'],
                                 stats['grabs'],
                                 stats['drops'],
                                 stats['hold'],
                                 stats['captures'],
                                 stats['prevent'],
                                 stats['returns'],
                                 stats['support'],
                                 stats['pups'])
                delete_pending_match_stats(match_id)
                delete_pending_match(match_id)
        except postgresql.exceptions.ForeignKeyError:
            abort(400, "Inexistent player id.")
        return "Match validated"

    @api.marshal_with(api.models['Message'])
    def delete(self, match_id):
        delete_pending_match_stats(match_id)
        delete_pending_match(match_id)
        return {
            'message': 'Match validated',
            'value': new_match_id,
        }
