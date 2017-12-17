# -*- coding: utf-8 -*-

import orm
from flask_restplus import abort
from flask_jwt_extended import create_access_token
# import postgresql.exceptions


def login(login, password):
    if orm.auth_admin.first(login, password):
        user = orm.to_json(orm.get_user_by_trigram.first(login))
        return {
            'message': 'Auth successful',
            'Bearer': create_access_token(identity=user['id'])
        }
    abort(401)


def create(user_id, password):
    orm.promote_user(user_id, password)
    return {
        'message': 'User promoted to admin.'
    }


def delete(user_id):
    orm.block_admin(user_id)
    return {
        'message': 'Admin downgraded to simple user'
    }
