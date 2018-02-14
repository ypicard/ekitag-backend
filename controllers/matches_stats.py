# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
# from flask_jwt_extended import create_access_token
import postgresql.exceptions


def index(match_id):
    stats = orm.to_json(orm.get_match_stats(match_id))
    if stats is None:
        abort(404, "Stats not found")
    return stats


def create(match_id, user_id, score, tags, popped, grabs, drops, hold, captures, prevent, returns, support, pups):
    try:
        stats_id = orm.create_pending_stats.first(match_id,
                                                user_id,
                                                score,
                                                tags,
                                                popped,
                                                grabs,
                                                drops,
                                                hold,
                                                captures,
                                                prevent,
                                                returns,
                                                support,
                                                pups)
    except postgresql.exceptions.ForeignKeyError:
        abort(404, "Match not found")
    return {
        'message': 'Stats created',
        'value': stats_id,
    }
