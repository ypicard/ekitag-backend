import orm

history = orm.to_json(orm.get_musigma_team())


seen_ids = []
nb = 0
orm.drop_musigma_team()
for m in history:
    if m['user_id'] not in seen_ids:
        seen_ids.append(m['user_id'])
        nb += 1
        orm.temp_copy(m['user_id'], None, None, 0, 25, 8.333333333333334)
    orm.temp_copy(m['user_id'], m['season_id'], m['match_id'], m['exposition'], m['mu'], m['sigma'])
    nb += 1


print(len(history))
print(seen_ids)
print(len(seen_ids))
print(nb)
