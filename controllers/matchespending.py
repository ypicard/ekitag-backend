# -*- coding: utf-8 -*-

import orm
from . import matches as matches_controller
from . import matches_stats as matches_stats_controller
from . import matchespending_stats as matchespending_stats_controller
from . import seasons as seasons_controller
from . import seasons_matches as seasons_matches_controller
from flask_restplus import abort
import musigma_team_global
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


def convert(match_id, validator):
   
    pending_match = orm.to_json(orm.get_pending_match_by_id.first(match_id))
    pending_stats = orm.to_json(orm.get_pending_match_stats(match_id))

    if pending_match is None:
        abort(404, "Pending match not found")

    # lol
    b1_id = orm.get_user_by_pseudo.first(pending_match['b1_pseudo'])
    b2_id = orm.get_user_by_pseudo.first(pending_match['b2_pseudo'])
    b3_id = orm.get_user_by_pseudo.first(pending_match['b3_pseudo'])
    b4_id = orm.get_user_by_pseudo.first(pending_match['b4_pseudo'])
    b5_id = orm.get_user_by_pseudo.first(pending_match['b5_pseudo'])
    b6_id = orm.get_user_by_pseudo.first(pending_match['b6_pseudo'])
    r1_id = orm.get_user_by_pseudo.first(pending_match['r1_pseudo'])
    r2_id = orm.get_user_by_pseudo.first(pending_match['r2_pseudo'])
    r3_id = orm.get_user_by_pseudo.first(pending_match['r3_pseudo'])
    r4_id = orm.get_user_by_pseudo.first(pending_match['r4_pseudo'])
    r5_id = orm.get_user_by_pseudo.first(pending_match['r5_pseudo'])
    r6_id = orm.get_user_by_pseudo.first(pending_match['r6_pseudo'])

    pseudo_id_map = {}
    pseudo_id_map[pending_match['b1_pseudo']] = b1_id
    pseudo_id_map[pending_match['b2_pseudo']] = b2_id
    pseudo_id_map[pending_match['b3_pseudo']] = b3_id
    pseudo_id_map[pending_match['b4_pseudo']] = b4_id
    pseudo_id_map[pending_match['b5_pseudo']] = b5_id
    pseudo_id_map[pending_match['b6_pseudo']] = b6_id
    pseudo_id_map[pending_match['r1_pseudo']] = r1_id
    pseudo_id_map[pending_match['r2_pseudo']] = r2_id
    pseudo_id_map[pending_match['r3_pseudo']] = r3_id
    pseudo_id_map[pending_match['r4_pseudo']] = r4_id
    pseudo_id_map[pending_match['r5_pseudo']] = r5_id
    pseudo_id_map[pending_match['r6_pseudo']] = r6_id

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
            # Update algo
            musigma_team_global.update([r1_id, r2_id, r3_id, r4_id, r5_id, r6_id], 
                                        [b1_id, b2_id, b3_id, b4_id, b5_id, b6_id],
                                         pending_match['r_score'],
                                         pending_match['b_score'])
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
