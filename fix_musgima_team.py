import orm

history = orm.to_json(orm.get_musigma_team())


seen_user_ids = []
seen_season_ids = {}
nb = 0
orm.drop_musigma_team()
for m in history:
    if m['season_id']:
        print(m['season_id'])
        if m['season_id'] not in seen_season_ids:
            seen_season_ids[m['season_id']] = []
        if m['user_id'] not in seen_season_ids[m['season_id']]:
            orm.create_user_musigma_team(m['user_id'], None, m['season_id'], 0, 25, 8.333333333333334)
            nb += 1
        orm.create_user_musigma_team(m['user_id'], m['match_id'], m['season_id'],  m['exposition'], m['mu'], m['sigma'])    
        nb += 1
    else:
        if m['user_id'] not in seen_user_ids:
            seen_user_ids.append(m['user_id'])
            orm.create_user_musigma_team(m['user_id'], None, None, 0, 25, 8.333333333333334)
            nb += 1
        orm.create_user_musigma_team(m['user_id'], m['match_id'], m['season_id'], m['exposition'], m['mu'], m['sigma'])
        nb += 1


print(len(history))
print(seen_user_ids)
print(len(seen_user_ids))
print(nb)
