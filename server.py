# -*- coding: utf-8 -*-
from flask import Flask
from flask_restplus import Api, Resource, reqparse, abort
from flask_restplus.inputs import datetime_from_iso8601
from flask_jwt_extended import JWTManager, create_access_token
from flask_sslify import SSLify
from flask_cors import CORS

import postgresql.exceptions
import postgresql.types

import datetime

from views import createViews
from orm import *
from utils import admin_required
import config

# ========================= INIT

secret = config.secret()
_app = Flask(__name__)
_app.config['JWT_SECRET_KEY'] = secret.get('secret')
_sslify = SSLify(_app)
_cors = CORS(_app)
_jwt = JWTManager(_app)
api = Api(_app,
          version="alpha",
          title="EkiTag API",
          description="Custom tagpro matchmaking and ranking API",
          authorizations={
              'admin': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization',
              }
          })

createViews(api)

# ========================= INPUT PARSERS

parser_create_user = reqparse.RequestParser()
parser_create_user.add_argument('pseudo', type=str, required=True, location='form')
parser_create_user.add_argument('trigram', type=str, required=True, location='form')

parser_login = reqparse.RequestParser()
parser_login.add_argument('login', type=str, required=True, location='form')
parser_login.add_argument('password', type=str, required=True, location='form')

parser_update_user = reqparse.RequestParser()
parser_update_user.add_argument('pseudo', type=str, required=True, location='form')
parser_update_user.add_argument('usual_pseudos', type=str, required=True, action='append', location='form')

parser_promote = reqparse.RequestParser()
parser_promote.add_argument('password', type=str, required=True, location='form')

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

parser_create_stats = reqparse.RequestParser()
parser_create_stats.add_argument('user_pseudo', type=str, required=True, location='form')
parser_create_stats.add_argument('score', type=int, location='form')
parser_create_stats.add_argument('tags', type=int, location='form')
parser_create_stats.add_argument('popped', type=int, location='form')
parser_create_stats.add_argument('grabs', type=int, location='form')
parser_create_stats.add_argument('drops', type=int, location='form')
parser_create_stats.add_argument('hold', type=float, location='form')
parser_create_stats.add_argument('captures', type=int, location='form')
parser_create_stats.add_argument('prevent', type=float, location='form')
parser_create_stats.add_argument('returns', type=int, location='form')
parser_create_stats.add_argument('support', type=int, location='form')
parser_create_stats.add_argument('pups', type=int, location='form')

parser_create_match = reqparse.RequestParser()
parser_create_match.add_argument('b_score', type=int, required=True, location='form')
parser_create_match.add_argument('r_score', type=int, required=True, location='form')
parser_create_match.add_argument('datetime', type=str, required=True, location='form')
parser_create_match.add_argument('b1_pseudo', type=str, required=True, location='form')
parser_create_match.add_argument('b2_pseudo', type=str, location='form')
parser_create_match.add_argument('b3_pseudo', type=str, location='form')
parser_create_match.add_argument('b4_pseudo', type=str, location='form')
parser_create_match.add_argument('b5_pseudo', type=str, location='form')
parser_create_match.add_argument('b6_pseudo', type=str, location='form')
parser_create_match.add_argument('r1_pseudo', type=str, required=True, location='form')
parser_create_match.add_argument('r2_pseudo', type=str, location='form')
parser_create_match.add_argument('r3_pseudo', type=str, location='form')
parser_create_match.add_argument('r4_pseudo', type=str, location='form')
parser_create_match.add_argument('r5_pseudo', type=str, location='form')
parser_create_match.add_argument('r6_pseudo', type=str, location='form')

parser_create_season = reqparse.RequestParser()
parser_create_season.add_argument('max_time', type=float, required=True, location='form')
parser_create_season.add_argument('max_matches', type=int, required=True, location='form')
parser_create_season.add_argument('name', type=str, required=True, location='form')


# ========================= GETTERS

def app():
    """Return the app object.

    Returns:
        the app object.

    """
    return _app


# ========================= NAMESPACE V1
v1 = api.namespace(name="v1", validate=True)


# ------------------------- USERS
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
            abort(404, "No users")
        return users


@v1.route("/users/<int:user_id>")
class User(Resource):
    @api.marshal_with(api.models['User'])
    def get(self, user_id):
        user = to_json(get_user_by_id.first(user_id))
        if user is None:
            abort(404, "User not found")
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
    @api.doc(security='admin')
    @admin_required
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
            abort(404, "No matches found")
        return matches


# ------------------------- ADMIN
@v1.route("/admin/")
class AdminAuth(Resource):
    @api.expect(parser_login)
    @api.marshal_with(api.models['Auth'])
    def post(self):
        args = parser_login.parse_args()
        if auth_admin.first(args['login'], args['password']):
            user = to_json(get_user_by_trigram.first(args['login']))
            return {
                'message': 'Auth successful',
                'Bearer': create_access_token(identity=user['id'])
            }
        abort(401)


@v1.route("/users/<int:user_id>/promote")
class UserPromote(Resource):
    @api.expect(parser_promote)
    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def post(self, user_id):
        args = parser_promote.parse_args()
        promote_user(user_id, args['password'])
        return {
            'message': 'User promoted to admin.'
        }

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, user_id):
        block_admin(user_id)
        return {
            'message': 'Admin downgraded to simple user'
        }


# ------------------------- MATCHES
@v1.route("/matches")
class Matches(Resource):
    @api.marshal_with(api.models['MatchMin'], as_list=True)
    def get(self):
        matches = to_json(get_matches())
        if matches is None:
            abort(404, "No matches found")
        return matches


@v1.route("/matches/<int:match_id>")
class Match(Resource):
    @api.marshal_with(api.models['Match'])
    def get(self, match_id):
        match = to_json(get_match_by_id.first(match_id))
        if match is None:
            abort(404, "Match not found")
        return match

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, match_id):
        delete_match_stats(match_id)
        remove_match_season(match_id)
        delete_match(match_id)
        return {
            'message': 'Match deleted',
        }


@v1.route("/matches/<int:match_id>/stats")
class MatchStats(Resource):
    @api.marshal_with(api.models['StatMin'], as_list=True)
    def get(self, match_id):
        stats = to_json(get_match_stats(match_id))
        if stats is None:
            abort(404, "Stats not found")
        return stats


@v1.route("/matches/pending")
class MatchesPending(Resource):
    @api.marshal_with(api.models['MatchPending'], as_list=True)
    def get(self):
        matches = to_json(get_pending_matches())
        if matches is None:
            abort(404, "No pending matches")
        return matches

    @api.expect(parser_create_match)
    @api.marshal_with(api.models['Message'])
    def post(self):
        args = parser_create_match.parse_args()
        new_match_id = create_pending_match.first(args['b_score'],
                                                  args['r_score'],
                                                  datetime_from_iso8601(args['datetime']),
                                                  args['b1_pseudo'],
                                                  args['b2_pseudo'],
                                                  args['b3_pseudo'],
                                                  args['b4_pseudo'],
                                                  args['b5_pseudo'],
                                                  args['b6_pseudo'],
                                                  args['r1_pseudo'],
                                                  args['r2_pseudo'],
                                                  args['r3_pseudo'],
                                                  args['r4_pseudo'],
                                                  args['r5_pseudo'],
                                                  args['r6_pseudo'])
        return {
            'message': 'Pending match created, waiting validation',
            'value': new_match_id,
        }


@v1.route("/matches/pending/<int:match_id>")
class MatchPending(Resource):
    @api.marshal_with(api.models['MatchPending'])
    def get(self, match_id):
        match = to_json(get_pending_match_by_id.first(match_id))
        if match is None:
            abort(404, "Pending match not found")
        return match

    @api.expect(parser_validate_match)
    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def put(self, match_id):
        def mapper(color):
            for i in range(1, 7):
                pseudo_id_map[pending_match[color + str(i) + "_pseudo"]] = args[color + str(i) + "_id"]
        args = parser_validate_match.parse_args()
        pending_match = to_json(get_pending_match_by_id.first(match_id))
        pending_stats = to_json(get_pending_match_stats(match_id))
        if pending_match is None:
            abort(404, "Pending match not found")
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
                season = to_json(get_running_season.first())
                if season is not None:
                    add_season_match(season['id'], new_match_id)
                    update_season_match_count(season['id'])
                    if pending_match['datetime'] >= season['start_time'] + season['max_time'] or season['played_matches'] + 1 >= season['max_matches']:
                        # TODO update stars
                        terminate_season(season_id, datetime.datetime.now())
        except postgresql.exceptions.ForeignKeyError:
            abort(400, "Inexistent player id.")
        return {
            'message': 'Match validated',
            'value': new_match_id,
        }

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, match_id):
        delete_pending_match_stats(match_id)
        delete_pending_match(match_id)
        return {
            'message': 'Match deleted',
        }


@v1.route("/matches/pending/<int:match_id>/stats")
class MatchPendingStats(Resource):
    @api.marshal_with(api.models['StatMin'], as_list=True)
    def get(self, match_id):
        stats = to_json(get_pending_match_stats(match_id))
        if stats is None:
            abort(404, "Stats not found")
        return stats

    @api.marshal_with(api.models['Message'])
    @api.expect(parser_create_stats)
    def post(self, match_id):
        args = parser_create_stats.parse_args()
        count = count_pending_stats_for_user_by_match.first(match_id, args['user_pseudo'])
        if count > 0:
            abort(400, "Stats already saved for this player")
        count = count_user_in_pending_match.first(match_id, args['user_pseudo'])
        if count == 0:
            abort(400, "Given player has not played in this match")
        stats_id = None
        try:
            stats_id = create_pending_stats.first(match_id,
                                                  args['user_pseudo'],
                                                  args['score'],
                                                  args['tags'],
                                                  args['popped'],
                                                  args['grabs'],
                                                  args['drops'],
                                                  datetime.timedelta(seconds=args['hold']),
                                                  args['captures'],
                                                  datetime.timedelta(seconds=args['prevent']),
                                                  args['returns'],
                                                  args['support'],
                                                  args['pups'])
        except postgresql.exceptions.ForeignKeyError:
            abort(404, "Match not found")
        return {
            'message': 'Stats created',
            'value': stats_id,
        }


# ------------------------- SEASONS
@v1.route("/seasons")
class Seasons(Resource):
    @api.marshal_with(api.models['Season'], as_list=True)
    def get(self):
        seasons = to_json(get_seasons())
        if seasons is None:
            abort(404, "No seasons found")
        return seasons

    @api.marshal_with(api.models['Message'])
    @api.expect(parser_create_season)
    @api.doc(security='admin')
    @admin_required
    def post(self):
        args = parser_create_season.parse_args()
        count = count_running_seasons.first()
        if count > 0:
            abort(400, "A season is already running, please terminate it before creating a new one.")
        new_season_id = create_season.first(args['name'], datetime.timedelta(seconds=args['max_time']), args['max_matches'], datetime.datetime.now())
        return {
            'message': 'New season launched',
            'values': new_season_id,
        }


@v1.route("/seasons/<int:season_id>")
class Season(Resource):
    @api.marshal_with(api.models['Season'])
    def get(self, season_id):
        season = to_json(get_season_by_id.first(season_id))
        if season is None:
            abort(404, "Season not found")
        return season

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, season_id):
        # TODO : update stars
        terminate_season(season_id, datetime.datetime.now())
        return {
            'message': 'Season finished',
        }


@v1.route("/seasons/<int:season_id>/matches")
class SeasonMatches(Resource):
    @api.marshal_with(api.models['MatchMin'], as_list=True)
    def get(self, season_id):
        matches = to_json(get_season_matches(season_id))
        if matches is None:
            abort(404, "Season not found")
        return matches
