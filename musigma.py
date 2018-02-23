# -*- coding: utf-8 -*-po

from trueskill import TrueSkill, Rating, rate_1vs1
from config import musigma
import itertools

config = musigma()
musigma_team = TrueSkill(mu=str(config.get('mu')),
                         sigma=str(config.get('sigma')),
                         beta=str(config.get('beta_team')),
                         tau=str(config.get('tau_team')),
                         draw_probability=str(config.get('epsilon_p_team')),
                         backend='mpmath')
musigma_solo = TrueSkill(mu=config.get('mu'),
                         sigma=config.get('sigma'),
                         beta=config.get('beta_solo'),
                         tau=config.get('tau_solo'),
                         draw_probability=config.get('epsilon_p_solo'),
                         backend='mpmath')


def get_all_possible_matches(ids):
    n = len(ids) // 2
    all_teams = list(itertools.combinations(ids, n))
    matches = []
    for t1 in all_teams:
        for t2 in all_teams:
            if not any(p in t1 for p in t2):
                matches.append((t1, t2))
    return matches

r1 = Rating()
r2 = Rating()
print(r1, r2)
new_r1, new_r2 = rate_1vs1(r1, r2)
print(new_r1, new_r2)
print(new_r1.mu)