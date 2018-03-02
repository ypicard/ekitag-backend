# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
# from flask_jwt_extended import create_access_token
# import postgresql.exceptions


def index():
    matches = orm.to_json(orm.get_matches())
    if matches is None:
        abort(404, "No matches found")
    return matches


def create(b_score, r_score, datetime, b1_id, b2_id, b3_id, b4_id, b5_id, b6_id, r1_id, r2_id, r3_id, r4_id, r5_id, r6_id, validator):
    new_match_id = orm.create_match.first(b_score,
                                        r_score,
                                        datetime,
                                        b1_id,
                                        b2_id,
                                        b3_id,
                                        b4_id,
                                        b5_id,
                                        b6_id,
                                        r1_id,
                                        r2_id,
                                        r3_id,
                                        r4_id,
                                        r5_id,
                                        r6_id,
                                        validator)
    return {
        'message': 'Pending match created, waiting validation',
        'value': new_match_id,
    }


def show(match_id):
    match = orm.to_json(orm.get_match_by_id.first(match_id))
    if match is None:
        abort(404, "Match not found")
    return match


def delete(match_id):
    orm.delete_match_stats(match_id)
    orm.remove_match_season(match_id)
    orm.delete_match(match_id)
    return {
        'message': 'Match deleted',
    }