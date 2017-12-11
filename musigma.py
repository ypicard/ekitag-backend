# -*- coding: utf-8 -*-
from trueskill import TrueSkill
from config import musigma
import itertools

config = musigma()
musigma_team = TrueSkill(mu=config.get('mu'),
                         sigma=config.get('sigma'),
                         beta=config.get('beta_team'),
                         tau=config.get('tau_team'),
                         draw_probability=config.get('epsilon_p_team'),
                         backend='mpmath')
musigma_solo = TrueSkill(mu=config.get('mu'),
                         sigma=config.get('sigma'),
                         beta=config.get('beta_solo'),
                         tau=config.get('tau_solo'),
                         draw_probability=config.get('epsilon_p_solo'),
                         backend='mpmath')


def comb_and_comp(lst, n, half=False):
    m = len(lst)
    if m < n:
        return
    if n == 0 or lst == []:
        yield [], lst
    else:
        first, rest = lst[0], lst[1:]
        for in_, out in comb_and_comp(rest, n - 1):
            yield [first] + in_, out
        for in_, out in comb_and_comp(rest, n):
            if half and in_[0] == lst[m // 2]:
                break
            yield in_, [first] + out


def get_all_equal_teams(ids):
    n = len(ids)
    h = n // 2
    return comb_and_comp(ids, h, n == h * 2)


def get_all_possible_teams(ids):
    return itertools.chain(*[comb_and_comp(ids, i, len(ids) == i * 2) for i in range(1, len(ids) // 2 + 1)])

print(list(get_all_equal_teams([1,2,3,4])))
print(len(list(get_all_equal_teams([1,2,3,4]))))