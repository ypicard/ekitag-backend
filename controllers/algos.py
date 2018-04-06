# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
from algos import musigma_team
import postgresql.exceptions
import logging

logger = logging.getLogger()


def show(algo, user_id):
    show_func = {'musigma_team': orm.get_all_user_musigma_rankings}[algo]
    return orm.to_json(show_func(user_id))


def run(algo, ids):
    logger.debug("ids: {}".format(ids))
    if (len(ids) < 2):
        abort(400, 'Not enough players')
    cur_season = orm.to_json(orm.get_running_season.first())
    cur_season_id = cur_season['id'] if cur_season else None
    logger.debug("current season id: {}".format(cur_season_id))
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


def index(algo, season_id):
    res = orm.to_json({
        'musigma_team': orm.get_ranked_users_musigma_team
    }[algo](season_id))

    ranking = { 'algo': algo,
                'users': [{'id': o['user_id'],
                          'pseudo': o['pseudo'],
                          'usual_pseudos': o['usual_pseudos'],
                          'is_active': o['is_active'],
                          'exposition': o['exposition'],
                          'mu': o['mu'],
                          'sigma': o['sigma'],
                          'rank': o['rank']} for o in res]}
    return ranking


def viz(algo, user_id, viz):
    # Put your different viz requests here
    res = orm.to_json({
        'musigma_team':{
            'history': orm.get_user_musigma_team_history
        }
    }[algo][viz](user_id))
    return { viz: res }
