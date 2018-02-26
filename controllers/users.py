# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
import postgresql.exceptions
from config import musigma_team_global, musigma_team_season

config_tg = musigma_team_global()
config_ts = musigma_team_season()

def index():
    users = orm.to_json(orm.get_users())
    if users is None:
        abort(404, "No users")
    return users


def create(trigram, pseudo):
    trigram = trigram.lower() # Always lowercase trigram
    try:
        user_id = orm.create_user.first(trigram, pseudo)
        # user_tg_id = orm.create_user_musigma_team.first(user_id, config_tg.get('mu'), config_tg.get('sigma'), None)
        # season = orm.to_json(orm.get_running_season.first())
        # if season:
        #     user_ts_id = orm.create_user_musigma_team.first(user_id, config_tg.get('mu'), config_tg.get('sigma'), season['id'])
    except postgresql.exceptions.UniqueError:
        abort(400, "Duplicated user")
    return {
        'message': 'User created',
        'value': user_id,
    }


def show(user_id):
    user = orm.to_json(orm.get_user_by_id.first(user_id))
    if user is None:
        abort(404, "User not found")
    return user


def update(user_id, pseudo, usual_pseudos):
    orm.update_user(user_id, pseudo, usual_pseudos)
    return {
        'message': 'User updated',
    }


def delete(user_id):
    orm.desactivate_user(user_id)
    return {
        'message': 'User deleted'
    }
