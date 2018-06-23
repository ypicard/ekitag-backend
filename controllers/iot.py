# -*- coding: utf-8 -*-

from flask_restplus import abort
import requests
import config

secret = config.secret()


def ping(duration=None):
    params = {}
    if duration: 
        params['duration'] = duration
    r = requests.get(secret.get('iot_uri') + '/tagpro', params=params)
    return {'message': 'Bip - boop - bip',
            'iot': r.status_code}
