# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
from algos import musigma_team
import postgresql.exceptions

def show(algo, ids):
    if (len(ids) < 2):
        abort(400, 'Not enough players')
    cur_season = orm.to_json(orm.get_running_season.first())
    cur_season_id = cur_season['id'] if cur_season else None
    return {'musigma_team': musigma_team.show}[algo](ids, cur_season_id)


def update(match_id, **kwargs):
    # TODO: Some work will be needed here when adding new algos
    cur_season = orm.to_json(orm.get_running_season.first())
    cur_season_id = cur_season['id'] if cur_season else None

    update_funcs = [musigma_team.update]

    # Update season and global for each algo available
    for update_func in update_funcs:
        update_func(match_id, None, **kwargs)
        if cur_season_id is not None:
            update_func(match_id, cur_season_id, **kwargs)

    return {
        'message': 'Algos updated'
    }
