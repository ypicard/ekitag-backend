# -*- coding: utf-8 -*-
from flask_restplus import fields


def createViews(api):
    api.model('Message', {
        'message': fields.String,
        'value': fields.Integer,
    })
    # ========================= USERS
    api.model('UserMin', {
        'id': fields.Integer,
        'pseudo': fields.String,
        # 'trigram': fields.String,
    })
    api.clone('User', api.models['UserMin'], {
        'gold_stars': fields.Integer,
        'silver_stars': fields.Integer,
        'copper_stars': fields.Integer,
        'loser_stars': fields.Integer,
        'is_active': fields.Boolean,
        'is_admin': fields.Boolean,
        'usual_pseudos': fields.List(fields.String),
    })

    # ========================= MATCHES
    api.model('MatchBase', {
        'id': fields.Integer,
        'r_score': fields.Integer,
        'b_score': fields.Integer,
        'datetime': fields.DateTime(dt_format="rfc822"),
    })
    api.clone('MatchValid', api.models['MatchBase'], {
        'validator': fields.Nested(api.models['UserMin'])
    })
    api.clone('MatchPending', api.models['MatchBase'], {
        'b1_pseudo': fields.String,
        'b2_pseudo': fields.String,
        'b3_pseudo': fields.String,
        'b4_pseudo': fields.String,
        'b5_pseudo': fields.String,
        'b6_pseudo': fields.String,
        'r1_pseudo': fields.String,
        'r2_pseudo': fields.String,
        'r3_pseudo': fields.String,
        'r4_pseudo': fields.String,
        'r5_pseudo': fields.String,
        'r6_pseudo': fields.String,
    })
    api.clone('MatchMin', api.models['MatchValid'], {
        'b1_id': fields.Integer,
        'b2_id': fields.Integer,
        'b3_id': fields.Integer,
        'b4_id': fields.Integer,
        'b5_id': fields.Integer,
        'b6_id': fields.Integer,
        'r1_id': fields.Integer,
        'r2_id': fields.Integer,
        'r3_id': fields.Integer,
        'r4_id': fields.Integer,
        'r5_id': fields.Integer,
        'r6_id': fields.Integer,
    })
    api.clone('Match', api.models['MatchValid'], {
        'b1': fields.Nested(api.models['UserMin']),
        'b2': fields.Nested(api.models['UserMin']),
        'b3': fields.Nested(api.models['UserMin']),
        'b4': fields.Nested(api.models['UserMin']),
        'b5': fields.Nested(api.models['UserMin']),
        'b6': fields.Nested(api.models['UserMin']),
        'r1': fields.Nested(api.models['UserMin']),
        'r2': fields.Nested(api.models['UserMin']),
        'r3': fields.Nested(api.models['UserMin']),
        'r4': fields.Nested(api.models['UserMin']),
        'r5': fields.Nested(api.models['UserMin']),
        'r6': fields.Nested(api.models['UserMin']),
    })

    # ========================= STATISTICS
    api.model('StatBase', {
        'id': fields.Integer,
        'match_id': fields.Integer,
        'score': fields.Integer,
        'tags': fields.Integer,
        'popped': fields.Integer,
        'grabs': fields.Integer,
        'drops': fields.Integer,
        'hold': fields.DateTime(dt_format="rfc822"),
        'captures': fields.Integer,
        'prevent': fields.DateTime(dt_format="rfc822"),
        'returns': fields.Integer,
        'support': fields.Integer,
        'pups': fields.Integer,
    })
    api.clone('StatPending', api.models['StatBase'], {
        'user_pseudo': fields.String,
    })
    api.clone('StatMin', api.models['StatBase'], {
        'user_id': fields.Integer,
    })
    api.clone('Stat', api.models['StatBase'], {
        'user': fields.Nested(api.models['UserMin']),
    })
