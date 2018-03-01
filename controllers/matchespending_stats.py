# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
# from flask_jwt_extended import create_access_token
import postgresql.exceptions


# def index(match_id):
#     stats = orm.to_json(orm.get_pending_match_stats(match_id))
#     if stats is None:
#         abort(404, "Stats not found")
#     return stats


def create(match_id, user_pseudo, score, tags, popped, grabs, drops, hold, captures, prevent, returns, support, pups):
    count = orm.count_pending_stats_for_user_by_match.first(match_id, user_pseudo)
    if count > 0:
        abort(400, "Stats already saved for this player")
    count = orm.count_user_in_pending_match.first(match_id, user_pseudo)
    if count == 0:
        abort(400, "Given player has not played in this match")
    stats_id = None
    try:
        stats_id = orm.create_pending_stats.first(match_id,
                                                  user_pseudo,
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


def delete_all(match_id):
    orm.delete_pending_match_stats(match_id)
