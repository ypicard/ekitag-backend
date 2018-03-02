# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restplus import Api, Resource
from flask_restplus.inputs import datetime_from_iso8601
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_sslify import SSLify
from flask_cors import CORS

import datetime

from views import createViews
from utils import admin_required
from parsers import *
import config
import orm
from controllers import users, users_matches, admin, matches, matches_stats, matchespending, matchespending_stats, seasons, seasons_matches, musigma_team

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
        return users.create(**args)

    @api.marshal_with(api.models['UserMin'], as_list=True)
    def get(self):
        return users.index()


@v1.route("/users/<int:user_id>")
class User(Resource):
    @api.marshal_with(api.models['User'])
    def get(self, user_id):
        return users.show(user_id)

    @api.marshal_with(api.models['Message'])
    @api.expect(parser_update_user)
    def put(self, user_id):
        args = parser_update_user.parse_args()
        return users.update(user_id, **args)

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, user_id):
        return users.delete(user_id)


@v1.route("/users/<int:user_id>/matches")
class UserMatches(Resource):
    @api.marshal_with(api.models['MatchMin'], as_list=True)
    def get(self, user_id):
        return users_matches.index(user_id)


# ------------------------- ADMIN
@v1.route("/admin/")
class AdminAuth(Resource):
    @api.expect(parser_login)
    @api.marshal_with(api.models['Auth'])
    def post(self):
        args = parser_login.parse_args()
        return admin.login(**args)


@v1.route("/users/<int:user_id>/promote")
class UserPromote(Resource):
    @api.expect(parser_promote)
    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def post(self, user_id):
        args = parser_promote.parse_args()
        return admin.create(user_id, **args)

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, user_id):
        return admin.delete(user_id)


# ------------------------- MATCHES
@v1.route("/matches")
class Matches(Resource):
    @api.marshal_with(api.models['MatchMin'], as_list=True)
    def get(self):
        return matches.index()


@v1.route("/matches/<int:match_id>")
class Match(Resource):
    @api.marshal_with(api.models['Match'])
    def get(self, match_id):
        return matches.show(match_id)

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, match_id):
        return matches.delete(match_id)


# @v1.route("/matches/<int:match_id>/stats")
# class MatchStats(Resource):
#     @api.marshal_with(api.models['StatMin'], as_list=True)
#     def get(self, match_id):
#         return matches_stats.index(match_id)


@v1.route("/matches/pending")
class MatchesPending(Resource):
    @api.marshal_with(api.models['MatchPending'], as_list=True)
    def get(self):
        return matchespending.index()

    @api.expect(parser_create_match)
    @api.marshal_with(api.models['Message'])
    def post(self):
        args = parser_create_match.parse_args()
        args['datetime'] = datetime_from_iso8601(args['datetime'])
        return matchespending.create(**args)


@v1.route("/matches/pending/<int:match_id>")
class MatchPending(Resource):
    @api.marshal_with(api.models['MatchPending'])
    def get(self, match_id):
        return matchespending.show(match_id)

    @api.expect(parser_validate_match)
    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def put(self, match_id):
        return matchespending.convert(match_id, validator=get_jwt_identity())

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, match_id):
        return matchespending.delete(match_id)

@v1.route("/matches/pending/<int:match_id>/stats")
class MatchPendingStats(Resource):
    # @api.marshal_with(api.models['StatMin'], as_list=True)
    # def get(self, match_id):
    #     return matchespending_stats.index(match_id)

    @api.marshal_with(api.models['Message'])
    @api.expect(parser_create_stats)
    def post(self, match_id):
        args = parser_create_stats.parse_args()
        if args['hold']:
            args['hold'] = datetime.timedelta(seconds=args['hold'])
        if args['prevent']:
            args['prevent'] = datetime.timedelta(seconds=args['prevent'])
        
        return matchespending_stats.create(match_id, **args)


# ------------------------- SEASONS
@v1.route("/seasons")
class Seasons(Resource):
    @api.marshal_with(api.models['Season'], as_list=True)
    def get(self):
        return seasons.index()

    @api.marshal_with(api.models['Message'])
    @api.expect(parser_create_season)
    @api.doc(security='admin')
    @admin_required
    def post(self):
        args = parser_create_season.parse_args()
        if args['max_time'] is not None:
            args['max_time'] = datetime.timedelta(seconds=args['max_time'])
        return seasons.create(**args)

@v1.route("/seasons/<int:season_id>")
class Season(Resource):
    @api.marshal_with(api.models['Season'])
    def get(self, season_id):
        return seasons.show(season_id)

    @api.marshal_with(api.models['Message'])
    @api.doc(security='admin')
    @admin_required
    def delete(self, season_id):
        return seasons.delete(season_id)


@v1.route("/seasons/<int:season_id>/matches")
class SeasonMatches(Resource):
    @api.marshal_with(api.models['MatchMin'], as_list=True)
    def get(self, season_id):
        return seasons_matches.index(season_id)

# ------------------------- ALGO: MUSIGMA_TEAM

@v1.route("/algo/musigma_team")
class MusigmaTeam(Resource):
    @api.marshal_with(api.models['MusigmaTeam'], as_list=True)
    @api.expect(parser_musigma_team_get)
    def get(self):
        args = parser_musigma_team_get.parse_args()
        cur_season = orm.to_json(orm.get_running_season.first())
        cur_season_id = cur_season['id'] if cur_season else None
        return musigma_team.show_next(cur_season_id, args['ids'])