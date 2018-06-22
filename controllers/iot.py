# -*- coding: utf-8 -*-

from flask_restplus import abort
import requests
import config

secret = config.secret()


def ping():
    r = requests.get(secret.get('iot_uri'))
    return {'message': 'Bip - boop - bip',
            'iot': r.status_code}
