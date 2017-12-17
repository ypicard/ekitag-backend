# -*- coding: utf-8 -*-

import orm
from . import matches as matches_controller
from . import matches_stats as matches_stats_controller
from . import matchespending_stats as matchespending_stats_controller
from . import seasons as seasons_controller
from . import seasons_matches as seasons_matches_controller
from flask_restplus import abort
# from flask_jwt_extended import create_access_token
import postgresql.exceptions


def index():
    matches = orm.to_json(orm.get_pending_matches())
    if matches is None:
        abort(404, "No pending matches")
    return matches


def create(b_score, r_score, datetime, b1_pseudo, b2_pseudo, b3_pseudo, b4_pseudo, b5_pseudo, b6_pseudo, r1_pseudo, r2_pseudo, r3_pseudo, r4_pseudo, r5_pseudo, r6_pseudo):
    new_match_id = orm.create_pending_match.first(b_score,
                                                  r_score,
                                                  datetime,
                                                  b1_pseudo,
                                                  b2_pseudo,
                                                  b3_pseudo,
                                                  b4_pseudo,
                                                  b5_pseudo,
                                                  b6_pseudo,
                                                  r1_pseudo,
                                                  r2_pseudo,
                                                  r3_pseudo,
                                                  r4_pseudo,
                                                  r5_pseudo,
                                                  r6_pseudo)
    return {
        'message': 'Pending match created, waiting validation',
        'value': new_match_id,
    }


def convert(match_id, validator, b1_id=None, b2_id=None, b3_id=None, b4_id=None, b5_id=None, b6_id=None, r1_id=None, r2_id=None, r3_id=None, r4_id=None, r5_id=None, r6_id=None):
    def mapper(color):
        for i in range(1, 7):
            pseudo_id_map[pending_match[color + str(i) + "_pseudo"]] = locals().get(color + str(i) + "_id")
    pending_match = orm.to_json(orm.get_pending_match_by_id.first(match_id))
    pending_stats = orm.to_json(orm.get_pending_match_stats(match_id))
    if pending_match is None:
        abort(404, "Pending match not found")
    pseudo_id_map = {}
    mapper('r')
    mapper('b')
    new_match_id = None
    try:
        with orm.transaction():
            new_match_id = matches_controller.create(pending_match['b_score'],
                                                     pending_match['r_score'],
                                                     pending_match['datetime'],
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
                                                     validator)['value']
            for stats in pending_stats:
                matches_stats_controller.create(new_match_id,
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
            matchespending_stats_controller.delete_all(new_match_id)
            delete(match_id)
            season = seasons_controller.show_current()
            if season is not None:
                seasons_matches_controller.create(season['id'], new_match_id)
    except postgresql.exceptions.ForeignKeyError:
        abort(400, "Something failed. Confident in all user ids ?")
    return {
        'message': 'Match validated',
        'value': new_match_id,
    }


def show(match_id):
    match = orm.to_json(orm.get_pending_match_by_id.first(match_id))
    if match is None:
        abort(404, "Pending match not found")
    return match


def delete(match_id):
    orm.delete_pending_match_stats(match_id)
    orm.delete_pending_match(match_id)
    return {
        'message': 'Match deleted',
    }
