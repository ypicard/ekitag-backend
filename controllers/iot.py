# -*- coding: utf-8 -*-

from flask_restplus import abort
from requests_futures.sessions import FuturesSession
import config

secret = config.secret()
session = FuturesSession()

def ping(duration=None):
    params = {}
    if duration: 
        params['duration'] = duration
    r = session.get(secret.get('iot_uri') + '/tagpro', params=params)
    return r