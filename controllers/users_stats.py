# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
# import postgresql.exceptions


# def index(user_id):
#     matches = orm.to_json(orm.get_user_matches(user_id))
#     if matches is None:
#         abort(404, "No matches found")
#     return matches

def get_user_custom_stats(user_id):
    stats = orm.to_json(orm.get_user_custom_stats.first(user_id))
    return stats


def get_user_match_stats(user_id):
    stats = orm.to_json(orm.get_user_match_stats.first(user_id))
    return stats
