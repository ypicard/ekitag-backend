# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
# import postgresql.exceptions


def index(user_id):
    matches = orm.to_json(orm.get_user_matches(user_id))
    if matches is None:
        abort(404, "No matches found")
    return matches
