# -*- coding: utf-8 -*-
from flask_restplus.fields import *
from timedelta import TimeDelta


def createViews(api):
    api.model('Message', {
        'message': String,
        'value': Integer,
    })
    api.model('Auth', {
        'message': String,
        'Bearer': String,
    })
    # ========================= USERS
    api.model('UserMin', {
        'id': Integer,
        'pseudo': String,
        'usual_pseudos': List(String, default=[]),
        'is_active': Boolean
        # 'trigram': String,
    })
    api.clone('User', api.models['UserMin'], {
        'gold_stars': Integer,
        'silver_stars': Integer,
        'copper_stars': Integer,
        'loser_stars': Integer,
        'is_active': Boolean,
        'is_admin': Boolean,
    })

    # ========================= MATCHES
    api.model('MatchBase', {
        'id': Integer,
        'r_score': Integer,
        'b_score': Integer,
        'datetime': DateTime(dt_format="iso8601"),
    })
    api.clone('MatchValid', api.models['MatchBase'], {
        'validator': Nested(api.models['UserMin'])
    })
    api.clone('MatchPending', api.models['MatchBase'], {
        'b1_pseudo': String,
        'b2_pseudo': String,
        'b3_pseudo': String,
        'b4_pseudo': String,
        'b5_pseudo': String,
        'b6_pseudo': String,
        'r1_pseudo': String,
        'r2_pseudo': String,
        'r3_pseudo': String,
        'r4_pseudo': String,
        'r5_pseudo': String,
        'r6_pseudo': String,
    })
    api.clone('MatchMin', api.models['MatchValid'], {
        'b1_id': Integer,
        'b2_id': Integer,
        'b3_id': Integer,
        'b4_id': Integer,
        'b5_id': Integer,
        'b6_id': Integer,
        'r1_id': Integer,
        'r2_id': Integer,
        'r3_id': Integer,
        'r4_id': Integer,
        'r5_id': Integer,
        'r6_id': Integer,
    })
    api.clone('Match', api.models['MatchValid'], {
        'b1': Nested(api.models['UserMin']),
        'b2': Nested(api.models['UserMin']),
        'b3': Nested(api.models['UserMin']),
        'b4': Nested(api.models['UserMin']),
        'b5': Nested(api.models['UserMin']),
        'b6': Nested(api.models['UserMin']),
        'r1': Nested(api.models['UserMin']),
        'r2': Nested(api.models['UserMin']),
        'r3': Nested(api.models['UserMin']),
        'r4': Nested(api.models['UserMin']),
        'r5': Nested(api.models['UserMin']),
        'r6': Nested(api.models['UserMin']),
    })

    # ========================= STATISTICS
    api.model('StatBase', {
        'id': Integer,
        'match_id': Integer,
        'score': Integer,
        'tags': Integer,
        'popped': Integer,
        'grabs': Integer,
        'drops': Integer,
        'hold': TimeDelta,
        'captures': Integer,
        'prevent': TimeDelta,
        'returns': Integer,
        'support': Integer,
        'pups': Integer,
    })
    api.clone('StatPending', api.models['StatBase'], {
        'user_pseudo': String,
    })
    api.clone('StatMin', api.models['StatBase'], {
        'user_id': Integer,
    })
    api.clone('Stat', api.models['StatBase'], {
        'user': Nested(api.models['UserMin']),
    })

    # ========================= SEASONS
    api.model('Season', {
        'id': Integer,
        'name': String,
        'start_time': DateTime(dt_format="iso8601"),
        'end_time': DateTime(dt_format="iso8601"),
        'max_time': TimeDelta,
        'played_matches': Integer,
        'max_matches': Integer,
        'running': Boolean,
    })

    # ========================= ALGO: MUSIGMA_TEAM
    api.model('MusigmaTeam', {
        'r_ids': List(Integer),
        'b_ids': List(Integer),
        'quality': Float
    })