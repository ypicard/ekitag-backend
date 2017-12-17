# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
# from flask_jwt_extended import create_access_token
# import postgresql.exceptions
import datetime


def index():
    seasons = orm.to_json(orm.get_seasons())
    if seasons is None:
        abort(404, "No seasons found")
    return seasons


def create(name, max_time, max_matches):
    count = orm.count_running_seasons.first()
    if count > 0:
        abort(400, "A season is already running, please terminate it before creating a new one.")
    new_season_id = orm.create_season.first(name, max_time, max_matches, datetime.datetime.now())
    return {
        'message': 'New season launched',
        'values': new_season_id,
    }


def show(season_id):
    season = orm.to_json(orm.get_season_by_id.first(season_id))
    if season is None:
        abort(404, "Season not found")
    return season


def delete(season_id):
    # TODO : update stars
    orm.terminate_season(season_id, datetime.datetime.now())
    return {
        'message': 'Season finished',
    }


def show_current():
    return orm.to_json(orm.get_running_season.first())
