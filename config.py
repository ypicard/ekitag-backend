# -*- coding: utf-8 -*-

import configparser
from pathlib import Path
import os
import sys

self = sys.modules[__name__]

self.__config = configparser.ConfigParser()
self.__config._interpolation = configparser.ExtendedInterpolation()

if not Path('secret.yml').exists():
    print("Looking for secrets in environment")
    env = os.environ['secret']
    if env is not None:
        self.__config.read_string(env)
    else:
        raise FileNotFoundError('No config available.')
else:
    self.__config.read('secret.yml')


def secret():
    return self.__config['DEFAULT']


def musigma_team_global():
    return self.__config['MUSIGMA_TEAM_GLOBAL']

def musigma_team_season():
    return self.__config['MUSIGMA_TEAM_SEASON']
