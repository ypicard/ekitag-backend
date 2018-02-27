# -*- coding: utf-8 -*-

from trueskill import TrueSkill, Rating, rate
from config import musigma_team_global, musigma_team_season
import itertools
import orm
from flask_restplus import abort

config_tg = musigma_team_global()
musigma_team_global = TrueSkill(mu=float(config_tg.get('mu')),
                         sigma=float(config_tg.get('sigma')),
                         beta=float(config_tg.get('beta')),
                         tau=float(config_tg.get('tau')),
                        #  draw_probability=float(config_tg.get('epsilon')),
                         backend='mpmath')

config_ts = musigma_team_season()
musigma_team_season = TrueSkill(mu=float(config_ts.get('mu')),
                         sigma=float(config_ts.get('sigma')),
                         beta=float(config_ts.get('beta')),
                         tau=float(config_ts.get('tau')),
                        #  draw_probability=float(config_ts.get('epsilon')),
                         backend='mpmath')

configs = {'global': musigma_team_global,
        'season': musigma_team_season }

def set_trueskill_env(name):
    configs[name].make_as_global()

def get_trueskill_env(name):
    return configs[name]

def update(r_ids, b_ids, r_score, b_score, season_id):

    def get_rates(ids):
        # Get musigma user / create it if none
        res = []
        for id in ids:
            pl = orm.to_json(orm.get_user_musigma_team.first(id, season_id))
            if pl is not None:
                res.append(Rating(float(pl['mu']), float(pl['sigma'])))
            else:
                res.append(Rating())
        return res

    env_name = 'global' if not season_id else 'season'
    set_trueskill_env(env_name)
    env = get_trueskill_env(env_name)

    r_ids = [id for id in r_ids if id is not None]
    b_ids = [id for id in b_ids if id is not None]

    r_rates = get_rates(r_ids)
    b_rates = get_rates(b_ids)

    new_r_rates, new_b_rates = rate([r_rates, b_rates], ranks=[b_score, r_score]) # Lower is better

    for idx, id in enumerate(r_ids):
        orm.upsert_user_musigma_team(id, new_r_rates[idx].mu, new_r_rates[idx].sigma, season_id)
    for idx, id in enumerate(b_ids):
        orm.upsert_user_musigma_team(id, new_b_rates[idx].mu, new_b_rates[idx].sigma, season_id)


def show_next(season_id, ids):
    if (len(ids) < 2):
        abort(400, 'Not enough players')

    env_name = 'global' if not season_id else 'season'
    set_trueskill_env(env_name)
    env = get_trueskill_env(env_name)

    players = { id: orm.to_json(orm.get_user_musigma_team.first(id, season_id)) for id in ids }
    rates = {id: Rating(p['mu'], p['sigma']) if p is not None else Rating() for (id, p) in players.items()}

    matches = get_all_possible_matches(ids)
    matches = [[{p: rates[p] for p in t} for t in m ] for m in matches]

    qualities = [env.quality(m) for m in matches]
    qual, idx = min((_, idx) for (idx, _) in enumerate(qualities))
    
    match = matches[idx]
    match = { 'r_ids': [id for id in match[0]],
            'b_ids': [id for id in match[1]],
            'quality': qual }
    return match


def get_all_possible_matches(ids):
    n = len(ids) // 2
    all_teams = list(itertools.combinations(ids, n))
    matches = []
    for t1 in all_teams:
        for t2 in all_teams:
            if not any(p in t1 for p in t2) and not any(t2 in m for m in matches):
                matches.append((t1, t2))
    return matches