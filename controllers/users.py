# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
import postgresql.exceptions
from config import musigma_team_global

config_mstg = musigma_team_global()

def index():
    users = orm.to_json(orm.get_users())
    if users is None:
        abort(404, "No users")
    return users


def create(trigram, pseudo):
    try:
        user_id = orm.create_user.first(trigram, pseudo)
        user_mstg_id = orm.create_user_musigma_team_global.first(user_id, config_mstg.get('mu'), config_mstg.get('sigma'))
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
