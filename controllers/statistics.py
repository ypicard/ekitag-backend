# -*- coding: utf-8 -*-

import orm
import config
secret = config.secret()
from flask_restplus import abort
import postgresql
import postgresql.exceptions
import postgresql.types

db = postgresql.open(secret.get('pg_uri'))

def rank(stat, method, season_id):
    res = orm.to_json(orm.get_ranking(stat, method, season_id))
    return {
        'stat': stat,
        'method': method,
        'ranking': res
    }


