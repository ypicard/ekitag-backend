# -*- coding: utf-8 -*-

import orm
from . import matches as matches_controller
from . import matches_stats as matches_stats_controller
from . import matchespending_stats as matchespending_stats_controller
from . import seasons as seasons_controller
from . import seasons_matches as seasons_matches_controller
from . import algos as algos_controller
from flask_restplus import abort
import postgresql.exceptions


def index():
    matches = orm.to_json(orm.get_pending_matches())
    if matches is None:
        abort(404, "No pending matches")
    return matches


def create(b_score, r_score, duration, datetime, b1_pseudo, b2_pseudo, b3_pseudo, b4_pseudo, b5_pseudo, b6_pseudo, r1_pseudo, r2_pseudo, r3_pseudo, r4_pseudo, r5_pseudo, r6_pseudo):
    print("FDP")
    if b1_pseudo is None or r1_pseudo is None:
        abort(403, 'Each team must have at lease one player.')

    # Check if match hasn't been submitted already
    last_match = orm.to_json(orm.get_last_pending_match.first())
    if last_match is not None and last_match['b_score'] == b_score and last_match['r_score'] == r_score and last_match['b1_pseudo'] == b1_pseudo and last_match['r1_pseudo'] == r1_pseudo and last_match['b2_pseudo'] == b2_pseudo and last_match['r2_pseudo'] == r2_pseudo and last_match['b3_pseudo'] == b3_pseudo and last_match['r3_pseudo'] == r3_pseudo:
        abort(403, 'Match already pendgin for validation.')

    new_match_id = orm.create_pending_match.first(b_score,
                                                  r_score,
                                                  duration,
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
    # pending_stats = orm.to_json(orm.get_pending_match_stats(match_id))
    if pending_match is None:
        abort(404, "Pending match not found")

    ids = {'r': [], 'b': []}
    for team in ['r', 'b']:
        for idx in range(1, 7):
            pseudo = pending_match[team + str(idx)]['user_pseudo']
            if pseudo is None:
                pending_match[team + str(idx)] = None
                continue

            player = orm.to_json(orm.get_user_by_pseudo.first(pseudo))
            if player is None:
                abort(400, "Pseudo {} can't be matched against existing players".format(pseudo))
            pending_match[team + str(idx)]['user_id'] = player['id']
            ids[team].append(player['id'])

    try:
        with orm.transaction():
            new_match_id = matches_controller.create(pending_match['b_score'],
                                                     pending_match['r_score'],
                                                     pending_match['duration'],
                                                     pending_match['datetime'],
                                                     pending_match['b1']['user_id'] if pending_match['b1'] else None,
                                                     pending_match['b2']['user_id'] if pending_match['b2'] else None,
                                                     pending_match['b3']['user_id'] if pending_match['b3'] else None,
                                                     pending_match['b4']['user_id'] if pending_match['b4'] else None,
                                                     pending_match['b5']['user_id'] if pending_match['b5'] else None,
                                                     pending_match['b6']['user_id'] if pending_match['b6'] else None,
                                                     pending_match['r1']['user_id'] if pending_match['r1'] else None,
                                                     pending_match['r2']['user_id'] if pending_match['r2'] else None,
                                                     pending_match['r3']['user_id'] if pending_match['r3'] else None,
                                                     pending_match['r4']['user_id'] if pending_match['r4'] else None,
                                                     pending_match['r5']['user_id'] if pending_match['r5'] else None,
                                                     pending_match['r6']['user_id'] if pending_match['r6'] else None,
                                                     validator)['value']

            for team in ['r', 'b']:
                for idx in range(1, 7):
                    player = pending_match[team + str(idx)]
                    if player is None:
                        continue
                    matches_stats_controller.create(new_match_id,
                                            player['user_id'],
                                            player['score'],
                                            player['tags'],
                                            player['popped'],
                                            player['grabs'],
                                            player['drops'],
                                            player['hold'],
                                            player['captures'],
                                            player['prevent'],
                                            player['returns'],
                                            player['support'],
                                            player['pups'])

            matchespending_stats_controller.delete_all(new_match_id)
            delete(match_id)

            # Link match to season
            season = seasons_controller.show_current()
            if season is not None:
                seasons_matches_controller.create(season['id'], new_match_id)

            # Update algo
            # TODO: All player stats will probably need to be passed here to update algo
            algos_controller.update(new_match_id,
                                    r_ids=ids['r'],
                                    b_ids=ids['b'],
                                    r_score=pending_match['r_score'],
                                    b_score=pending_match['b_score'])

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
