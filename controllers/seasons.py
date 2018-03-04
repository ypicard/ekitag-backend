# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
# from flask_jwt_extended import create_access_token
# import postgresql.exceptions
import datetime


def index():
    seasons = orm.to_json(orm.get_seasons())
    if seasons is None:
        abort(404, "No seasons found")
    return seasons


def create(name, max_time, max_matches):
    count = orm.count_running_seasons.first()
    if count > 0:
        abort(400, "A season is already running, please terminate it before creating a new one.")
    new_season_id = orm.create_season.first(name, max_time, max_matches, datetime.datetime.now())
    return {
        'message': 'New season launched',
        'values': new_season_id,
    }


def show(season_id):
    season = orm.to_json(orm.get_season_by_id.first(season_id))
    if season is None:
        abort(404, "Season not found")
    return season


def show_ranking(algo, season_id):
    # TODO: Should be moved to its own controller: Algo
    # TODO: Discover how to pass None as param for orm query and interpret it as NULL
    if season_id is not None:
        res = orm.to_json({ 
            'musigma_team': orm.get_ranked_users_musigma_team_season
        }[algo](season_id))
    else:
        res = orm.to_json({
            'musigma_team': orm.get_ranked_users_musigma_team_global
        }[algo]())

    ranking = {
        'id': res[0]['season_id'],
        'name': res[0]['season_name'],
        'start_time': res[0]['start_time'],
        'end_time': res[0]['end_time'],
        'max_time': res[0]['max_time'],
        'played_matches': res[0]['played_matches'],
        'max_matches': res[0]['max_matches'],
        'running': res[0]['running'],
        'algo': algo
    }
    ranking['users'] = [{ 'id': o['user_id'],
                                'pseudo': o['pseudo'],
                                'usual_pseudos': o['usual_pseudos'],
                                'is_active': o['is_active'],
                                'mu': o['mu'],
                                'sigma': o['sigma'],
                                'rank': o['rank'] } for o in res]
    return ranking


def delete(season_id):
    with orm.transaction():
        orm.terminate_season(season_id, datetime.datetime.now())
        # Award stars
        ranked_users = orm.to_json(orm.get_ranked_users_musigma_team(season_id))
    
        if len(ranked_users) > 1:
            orm.award_gold_star(ranked_users[0]['user_id'])
            orm.award_loser_star(ranked_users[-1]['user_id'])
        if len(ranked_users) > 2:
            orm.award_silver_star(ranked_users[1]['user_id'])
        if len(ranked_users) > 3:
            orm.award_copper_star(ranked_users[2]['user_id'])
    
    return {
        'message': 'Season finished',
    }


def show_current():
    return orm.to_json(orm.get_running_season.first())
