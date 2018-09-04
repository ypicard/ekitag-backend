# -*- coding: utf-8 -*-

import orm
import config
secret = config.secret()
from flask_restplus import abort
import postgresql
import postgresql.exceptions
import postgresql.types


def create(user_id, season_id, description, value):
    try:
        penalty_id = orm.create_penalty.first(user_id, season_id, description, value)
        
    except postgresql.exceptions.UniqueError:
        abort(400, "Duplicated penalty")
    return {
        'message': 'Penalty created',
        'value': penalty_id,
    }

def index(season_id=None):
    if season_id:
        penalties = orm.to_json(orm.get_season_penalties(season_id))
    else:
        penalties = orm.to_json(orm.get_penalties())

    if penalties is None:
        abort(404, "No penalties")
    return penalties
    
