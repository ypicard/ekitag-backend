# -*- coding: utf-8 -*-

from trueskill import TrueSkill, Rating
from config import musigma_team_global
import itertools
import orm

config_mstg = musigma_team_global()
musigma_team_global = TrueSkill(mu=str(config_mstg.get('mu')),
                         sigma=str(config_mstg.get('sigma')),
                         beta=str(config_mstg.get('beta')),
                         tau=str(config_mstg.get('tau')),
                         draw_probability=str(config_mstg.get('epsilon')),
                         backend='mpmath')

def update(r_ids, b_ids, r_score, b_score):
    reds = [orm.get_user_musigma_team_global_from_id(id) for id in r_ids]
    reds = [r for r in reds if r != []]
    blues = [orm.get_user_musigma_team_global_from_id(id) for id in b_ids]
    blues = [b for b in blues if b != []]
    if (len(reds + blues) != len(r_ids + b_ids)):
        abort(500, 'Not all players exist in musigma_team_global table')
    r_rates = [Rating(r.mu, r.sigma) for r in reds]
    b_rates = [Rating(b.mu, b.sigma) for b in blues]
    new_r_rates, new_b_rates = rate([r_rates, b_rates], ranks=[r_score, b_score])

    for idx, id in enumerate(r_ids):
        orm.update_user_musigma_team_global(id, new_r_rates[idx].mu, new_r_rates[idx].sigma)
    for idx, id in enumerate(b_ids):
        orm.update_user_musigma_team_global(id, new_b_rates[idx].mu, new_b_rates[idx].sigma)


def get_next_match(ids):
    players = orm.get_users_musigma_team_global_from_ids(ids)
    rates = [Rating(p.mu, p.sigma) for p in players]
    matches = get_all_possible_matches(ids)
    qualities = [rate(m) for m in matches]
    _, idx = min((_, idx) for (idx, _) in enumerate(qualities))
    return matches[idx]


def get_all_possible_matches(ids):
    n = len(ids) // 2
    all_teams = list(itertools.combinations(ids, n))
    matches = []
    for t1 in all_teams:
        for t2 in all_teams:
            if not any(p in t1 for p in t2):
                matches.append((t1, t2))
    return matches


r_ids = [9, 12]
b_ids = [11, 13]
update(r_ids, b_ids, 1, 0)
