# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
from . import seasons as seasons_controller
# from flask_jwt_extended import create_access_token
# import postgresql.exceptions


def index(season_id):
    matches = orm.to_json(orm.get_season_matches(season_id))
    if matches is None:
        abort(404, "Season not found")
    return matches


def create(season_id, match_id):
    new_id = orm.add_season_match.first(season_id, match_id)
    new_match = orm.to_json(orm.get_match_by_id.first(match_id))
    season = orm.to_json(orm.get_season_by_id.first(season_id))
    orm.update_season_match_count(season_id)
    if (season['max_time'] is not None and new_match['datetime'] >= season['start_time'] + season['max_time']) or \
        (season['max_matches'] is not None and season['played_matches'] + 1 >= season['max_matches']):
        seasons_controller.delete(season_id)
    return {
        'message': 'Match added to season',
        'value': new_id,
    }
