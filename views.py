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
        'bronze_stars': Integer,
        'loser_stars': Integer,
        'is_active': Boolean,
        'is_admin': Boolean,
    })
 
    # ========================= SEASONS
    api.model('SeasonMin', {
        'id': Integer,
        'name': String,
        'running': Boolean,
    })
    api.clone('Season', api.models['SeasonMin'], {
        'start_time': DateTime(dt_format="iso8601"),
        'end_time': DateTime(dt_format="iso8601"),
        'max_time': TimeDelta,
        'played_matches': Integer,
        'max_matches': Integer,
    })
    # ========================= ALGO
    api.model('AlgoUserMin', {
           'mu': Float,
           'sigma': Float,
           'exposition': Float,
           'rank': Integer
       })
    api.clone('AlgoUser', api.models['UserMin'], api.models['AlgoUserMin'])
    api.model('AlgoUsers', {
        'algo': String,
        'users': List(Nested(api.models['AlgoUser'])),
        })
    api.clone('AlgoUserMinSeason', api.models['AlgoUserMin'], {
        'season_id': Integer,
        'season_name': String
    })
    api.model('AlgoUserAll',  {
        'rankings': List(Nested(api.models['AlgoUserMinSeason']))
    })
    api.model('VizHistoryEl', {
        'mu': Float,
        'sigma': Float,
        'exposition': Float,
        'user_id': Integer,
        'season_id': Integer,
        'match_id': Integer,
        'datetime': DateTime(dt_format="iso8601")
    })
    api.model('AlgoUserVizHistory', {
        'history': List(Nested(api.models['VizHistoryEl']))
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
    api.model('UserCustomStats', {
        'avg_score': Float,
        'score_rating': Float,
        'avg_tags': Float,
        'tags_rating': Float,
        'avg_popped': Float,
        'popped_rating': Float,
        'avg_grabs': Float,
        'grabs_rating': Float,
        'avg_drops': Float,
        'drops_rating': Float,
        'avg_hold': TimeDelta,
        'hold_rating': Float,
        'avg_captures': Float,
        'captures_rating': Float,
        'avg_prevent': TimeDelta,
        'prevent_rating': Float,
        'avg_returns': Float,
        'returns_rating': Float,
        'avg_support': Float,
        'support_rating': Float,
        'avg_pups': Float,
        'pups_rating': Float
    })
    api.model('UserCustomMatchStats', {
        'matches_played': Integer,
        'wins': Integer,
        'losses': Integer,
        'ties': Integer,
        'avg_match_duration': TimeDelta,
        'avg_team_score': Float
    })

    # ========================= MATCHES
    api.model('MatchBase', {
        'id': Integer,
        'r_score': Integer,
        'b_score': Integer,
        'datetime': DateTime(dt_format="iso8601"),
        'duration': TimeDelta,
    })
    api.clone('MatchPending', api.models['MatchBase'], {
        'b1': Nested(api.models['StatPending']),
        'b2': Nested(api.models['StatPending']),
        'b3': Nested(api.models['StatPending']),
        'b4': Nested(api.models['StatPending']),
        'b5': Nested(api.models['StatPending']),
        'b6': Nested(api.models['StatPending']),
        'r1': Nested(api.models['StatPending']),
        'r2': Nested(api.models['StatPending']),
        'r3': Nested(api.models['StatPending']),
        'r4': Nested(api.models['StatPending']),
        'r5': Nested(api.models['StatPending']),
        'r6': Nested(api.models['StatPending']),
    })
    api.clone('MatchValid', api.models['MatchBase'], {
        'validator': Nested(api.models['UserMin']),
        'season': Nested(api.models['SeasonMin'])
    })
    api.clone('UserMatch', api.models['MatchBase'], {
        'output': String,
        'season': Nested(api.models['SeasonMin'])
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
        'r6_id': Integer
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
        'b1_stats': Nested(api.models['StatMin']),
        'b2_stats': Nested(api.models['StatMin']),
        'b3_stats': Nested(api.models['StatMin']),
        'b4_stats': Nested(api.models['StatMin']),
        'b5_stats': Nested(api.models['StatMin']),
        'b6_stats': Nested(api.models['StatMin']),
        'r1_stats': Nested(api.models['StatMin']),
        'r2_stats': Nested(api.models['StatMin']),
        'r3_stats': Nested(api.models['StatMin']),
        'r4_stats': Nested(api.models['StatMin']),
        'r5_stats': Nested(api.models['StatMin']),
        'r6_stats': Nested(api.models['StatMin'])
    })

    # ========================= ALGO
    api.model('Algo', {
        'r_ids': List(Integer),
        'b_ids': List(Integer),
        'quality': Float
    })
