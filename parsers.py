# -*- coding: utf-8 -*-

from flask_restplus import reqparse

# ========================= INPUT PARSERS

parser_create_user = reqparse.RequestParser()
parser_create_user.add_argument('pseudo', type=str, required=True, location='form')
parser_create_user.add_argument('trigram', type=str, required=True, location='form')

parser_login = reqparse.RequestParser()
parser_login.add_argument('login', type=str, required=True, location='form')
parser_login.add_argument('password', type=str, required=True, location='form')

parser_update_user = reqparse.RequestParser()
parser_update_user.add_argument('pseudo', type=str, required=True, location='form')
parser_update_user.add_argument('usual_pseudos', type=str, required=True, action='append', location='form')

parser_promote = reqparse.RequestParser()
parser_promote.add_argument('password', type=str, required=True, location='form')

parser_create_stats = reqparse.RequestParser()
parser_create_stats.add_argument('user_pseudo', type=str, required=True, location='form')
parser_create_stats.add_argument('score', type=int, location='form')
parser_create_stats.add_argument('tags', type=int, location='form')
parser_create_stats.add_argument('popped', type=int, location='form')
parser_create_stats.add_argument('grabs', type=int, location='form')
parser_create_stats.add_argument('drops', type=int, location='form')
parser_create_stats.add_argument('hold', type=float, location='form')
parser_create_stats.add_argument('captures', type=int, location='form')
parser_create_stats.add_argument('prevent', type=float, location='form')
parser_create_stats.add_argument('returns', type=int, location='form')
parser_create_stats.add_argument('support', type=int, location='form')
parser_create_stats.add_argument('pups', type=int, location='form')

parser_create_match = reqparse.RequestParser()
parser_create_match.add_argument('b_score', type=int, required=True, location='form')
parser_create_match.add_argument('r_score', type=int, required=True, location='form')
parser_create_match.add_argument('duration', type=float, location='form')
parser_create_match.add_argument('datetime', type=str, required=True, location='form')
parser_create_match.add_argument('b1_pseudo', type=str, required=True, location='form')
parser_create_match.add_argument('b2_pseudo', type=str, location='form')
parser_create_match.add_argument('b3_pseudo', type=str, location='form')
parser_create_match.add_argument('b4_pseudo', type=str, location='form')
parser_create_match.add_argument('b5_pseudo', type=str, location='form')
parser_create_match.add_argument('b6_pseudo', type=str, location='form')
parser_create_match.add_argument('r1_pseudo', type=str, required=True, location='form')
parser_create_match.add_argument('r2_pseudo', type=str, location='form')
parser_create_match.add_argument('r3_pseudo', type=str, location='form')
parser_create_match.add_argument('r4_pseudo', type=str, location='form')
parser_create_match.add_argument('r5_pseudo', type=str, location='form')
parser_create_match.add_argument('r6_pseudo', type=str, location='form')

parser_create_season = reqparse.RequestParser()
parser_create_season.add_argument('name', type=str, required=True, location='form')
parser_create_season.add_argument('max_time', type=float, location='form')
parser_create_season.add_argument('max_matches', type=int, location='form')

parser_musigma_team_get = reqparse.RequestParser()
parser_musigma_team_get.add_argument('ids', type=int, required=True, action='append', location='args')